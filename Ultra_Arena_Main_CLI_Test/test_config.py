#!/usr/bin/env python3
"""
Test Configuration for Ultra Arena Main CLI Tests

This module provides a centralized configuration system for managing test fixtures.
It allows easy switching between different test input file collections without affecting
other parts of the test suite.

Features:
- Multiple test fixture support
- Easy switching between different test collections
- Graceful handling of missing directories
- Validation of directory structure
- Default fallback configurations
"""

import logging
import os
import tempfile
from pathlib import Path
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test Configuration Constants
TEST_FIXTURE = "default_fixture"  # Single point of configuration - just change this!
REQUEST_TIMEOUT = 200  # Timeout in seconds for CLI operations (default: 200s)

def get_test_fixture_paths(fixture_name: str = None, use_temp_output: bool = True):
    """
    Get standardized paths for a test fixture by loading from fixture_config.py.
    
    Args:
        fixture_name: Name of the test fixture (defaults to TEST_FIXTURE)
        use_temp_output: If True, use a temporary directory for output instead of fixture's output_dir
    
    Returns:
        Dictionary with standardized paths for the test fixture
    
    Raises:
        FileNotFoundError: If fixture_config.py is missing
        Exception: If there's an error loading or parsing fixture_config.py
    """
    if fixture_name is None:
        fixture_name = TEST_FIXTURE
    
    base_dir = Path(__file__).parent
    fixture_dir = base_dir / "test_fixtures" / fixture_name
    
    # Load fixture_config.py from the test fixture
    fixture_config_path = fixture_dir / "fixture_config.py"
    
    if not fixture_config_path.exists():
        raise FileNotFoundError(f"fixture_config.py not found in {fixture_dir}. Each test fixture must have a fixture_config.py file.")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("fixture_config", fixture_config_path)
        fixture_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixture_config)
        
        # Get paths from fixture_config.py and resolve them relative to the fixture directory
        input_pdf_dir_path = fixture_dir / getattr(fixture_config, "INPUT_PDF_DIR_PATH", "input_files")
        benchmark_file_path = fixture_dir / getattr(fixture_config, "BENCHMARK_FILE_PATH", "benchmark_files/benchmark_252_files.xlsx")
        
        # Use temporary directory for output to prevent test artifacts in fixtures
        if use_temp_output:
            output_dir = tempfile.mkdtemp(prefix=f"test_output_{fixture_name}_")
            logger.info(f"📁 Using temporary output directory: {output_dir}")
        else:
            output_dir = fixture_dir / getattr(fixture_config, "OUTPUT_DIR", "output_files")
        
        prompt_config_path = fixture_dir / getattr(fixture_config, "PROMPT_CONFIG_PATH", "prompt_config.py")
        
        return {
            "input_pdf_dir_path": str(input_pdf_dir_path),
            "benchmark_file_path": str(benchmark_file_path),
            "output_dir": str(output_dir),
            "prompt_config_path": str(prompt_config_path)
        }
        
    except Exception as e:
        raise Exception(f"Error loading fixture_config.py from {fixture_dir}: {e}. Please check the file syntax and required variables.")

def cleanup_temp_output(output_dir: str):
    """
    Clean up temporary output directory after tests.
    
    Args:
        output_dir: Path to the temporary output directory to clean up
    """
    try:
        import shutil
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            logger.info(f"🧹 Cleaned up temporary output directory: {output_dir}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to clean up temporary output directory {output_dir}: {e}")

def list_available_test_fixtures():
    """
    List all available test fixtures.
    
    Returns:
        List of available test fixture names
    """
    base_dir = Path(__file__).parent
    test_fixtures_dir = base_dir / "test_fixtures"
    
    if not test_fixtures_dir.exists():
        return []
    
    return [d.name for d in test_fixtures_dir.iterdir() if d.is_dir()]

def load_prompt_config(fixture_name: str = None):
    """
    Load prompt configuration from a test fixture's fixture_config.py.
    
    Args:
        fixture_name: Name of the test fixture (defaults to TEST_FIXTURE)
    
    Returns:
        Dictionary with prompt configuration or None if not found
    """
    if fixture_name is None:
        fixture_name = TEST_FIXTURE
    
    paths = get_test_fixture_paths(fixture_name)
    fixture_dir = Path(paths["input_pdf_dir_path"]).parent.parent  # Go up to fixture directory
    fixture_config_path = fixture_dir / "fixture_config.py"
    
    if not fixture_config_path.exists():
        return None
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("fixture_config", fixture_config_path)
        fixture_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixture_config)
        
        return {
            "system_prompt": getattr(fixture_config, "SYSTEM_PROMPT", ""),
            "user_prompt": getattr(fixture_config, "USER_PROMPT", ""),
            "mandatory_keys": getattr(fixture_config, "MANDATORY_KEYS", []),
            "text_first_regex_criteria": getattr(fixture_config, "TEXT_FIRST_REGEX_CRITERIA", {})
        }
        
    except Exception as e:
        logger.error(f"Error loading prompt config from {fixture_config_path}: {e}")
        return None

# Alias functions for backward compatibility with existing tests
def get_test_profile_paths(profile_name: str = None):
    """
    Alias for get_test_fixture_paths for backward compatibility.
    
    Args:
        profile_name: Name of the test fixture (defaults to TEST_FIXTURE)
    
    Returns:
        Dictionary with standardized paths for the test fixture
    """
    return get_test_fixture_paths(profile_name)

def get_available_test_profiles():
    """
    Alias for list_available_test_fixtures for backward compatibility.
    
    Returns:
        List of available test fixture names
    """
    return list_available_test_fixtures()

if __name__ == "__main__":
    print("🧪 Ultra Arena Main CLI Test Configuration")
    print("=" * 50)
    
    print(f"\n📁 Current test fixture: {TEST_FIXTURE}")
    
    print(f"\n📂 Available test fixtures:")
    fixtures = list_available_test_fixtures()
    for fixture in fixtures:
        print(f"  - {fixture}")
    
    print(f"\n🔧 Example Usage:")
    print("from test_config import get_test_fixture_paths, load_prompt_config")
    print("paths = get_test_fixture_paths('default_fixture')")
    print("prompts = load_prompt_config('default_fixture')")
    print("print(f'Input path: {paths[\"input_pdf_dir_path\"]}')")
    print("print(f'System prompt: {prompts[\"system_prompt\"][:50]}...')") 