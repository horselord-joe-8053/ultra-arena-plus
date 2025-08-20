#!/usr/bin/env python3
"""
Ultra Arena Main CLI

This is the main CLI entry point for the Ultra Arena Main library.
It imports the main functions and provides a simple CLI wrapper with performance monitoring.
"""

import sys
import os
import logging
import argparse
from pathlib import Path
from typing import Any

# Add the Ultra_Arena_Main to the Python path
ultra_arena_main_path = Path(__file__).parent.parent / "Ultra_Arena_Main"
sys.path.insert(0, str(ultra_arena_main_path))

# Import the main functions from Ultra_Arena_Main
from main_modular import (
    setup_logging,
    run_combo_processing
)

# Import performance monitoring
from performance_measure import (
    time_operation,
    mark_point,
    track_memory
)

def inject_profile_config(profile_name: str) -> None:
    """
    Inject the specified profile configuration into the Ultra_Arena_Main library.
    
    This function dynamically switches the profile configuration before calling
    library functions to ensure they use the correct settings.
    
    Args:
        profile_name (str): Name of the profile to inject (e.g., 'default_profile_base')
    """
    try:
        import config.config_base as config_base
        
        # Load prompt configuration from CLI profile
        _load_cli_prompt_config()
        
    except Exception as e:
        logging.error(f"❌ Failed to inject profile config: {e}")
        raise

def _load_cli_prompt_config() -> None:
    """
    Load prompt configuration from CLI profile and inject into config_base.
    """
    try:
        import config.config_base as config_base
        import importlib.util
        
        # Load prompt configuration from CLI profile
        current_dir = Path(__file__).parent
        prompt_config_path = current_dir / "run_profiles" / "default_profile_cli" / "profile_prompts_config.py"
        
        if prompt_config_path.exists():
            spec = importlib.util.spec_from_file_location("profile_prompts_config", str(prompt_config_path))
            if spec and spec.loader:
                prompt_config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(prompt_config_module)
                
                # Inject prompt configuration into config_base
                if hasattr(prompt_config_module, 'SYSTEM_PROMPT'):
                    config_base.SYSTEM_PROMPT = prompt_config_module.SYSTEM_PROMPT
                    logging.info(f"📝 Loaded CLI SYSTEM_PROMPT from profile")
                if hasattr(prompt_config_module, 'USER_PROMPT'):
                    config_base.USER_PROMPT = prompt_config_module.USER_PROMPT
                    logging.info(f"📝 Loaded CLI USER_PROMPT from profile")
                if hasattr(prompt_config_module, 'JSON_FORMAT_INSTRUCTIONS'):
                    config_base.JSON_FORMAT_INSTRUCTIONS = prompt_config_module.JSON_FORMAT_INSTRUCTIONS
                    logging.info(f"📝 Loaded CLI JSON_FORMAT_INSTRUCTIONS from profile")
                if hasattr(prompt_config_module, 'MANDATORY_KEYS'):
                    config_base.MANDATORY_KEYS = prompt_config_module.MANDATORY_KEYS
                    logging.info(f"📝 Loaded CLI MANDATORY_KEYS from profile")
                if hasattr(prompt_config_module, 'TEXT_FIRST_REGEX_CRITERIA'):
                    config_base.TEXT_FIRST_REGEX_CRITERIA = prompt_config_module.TEXT_FIRST_REGEX_CRITERIA
                    logging.info(f"📝 Loaded CLI TEXT_FIRST_REGEX_CRITERIA from profile")
            else:
                logging.warning(f"⚠️ Could not load CLI prompt config from: {prompt_config_path}")
        else:
            logging.warning(f"⚠️ CLI prompt config file not found: {prompt_config_path}")
            
    except Exception as e:
        logging.error(f"❌ Failed to load CLI prompt configuration: {e}")
        raise

def _resolve_prompt_config_with_sources(prompt_overrides: dict, test_profile: str = None) -> dict:
    """
    Resolve prompt configuration with source tracking for CLI.
    
    Args:
        prompt_overrides: Dictionary containing command-line prompt overrides
        test_profile: Optional test profile name
        
    Returns:
        dict: Resolved prompt configuration with source information
    """
    import json
    
    # Initialize prompt configuration with source tracking
    prompt_config = {}
    all_prompts_with_source = {}
    
    # Define all possible prompt fields
    prompt_fields = [
        'system_prompt', 'user_prompt', 'json_format_instructions', 
        'mandatory_keys', 'text_first_regex_criteria'
    ]
    
    # Process each prompt field
    for field in prompt_fields:
        if field in prompt_overrides:
            # Command-line override takes highest priority
            prompt_config[field] = prompt_overrides[field]
            all_prompts_with_source[field] = {
                "value": prompt_overrides[field],
                "source": "cli_override"
            }
        else:
            # Check test profile defaults (if running in test mode)
            if test_profile:
                test_value = _get_test_profile_prompt_value(field, test_profile)
                if test_value is not None:
                    prompt_config[field] = test_value
                    all_prompts_with_source[field] = {
                        "value": test_value,
                        "source": "test_fixture"
                    }
                    continue
            
            # Check CLI profile defaults
            cli_value = _get_cli_profile_prompt_value(field)
            if cli_value is not None:
                prompt_config[field] = cli_value
                all_prompts_with_source[field] = {
                    "value": cli_value,
                    "source": "profile_default"
                }
            else:
                # Check system defaults
                system_value = _get_system_prompt_value(field)
                if system_value is not None:
                    prompt_config[field] = system_value
                    all_prompts_with_source[field] = {
                        "value": system_value,
                        "source": "system_default"
                    }
    
    # Log the complete prompt configuration with sources
    if all_prompts_with_source:
        logging.info(f"🔍 DETECTING PROMPT CONFIGURATION:")
        logging.info(f"   {'='*60}")
        logging.info(f"📄 PROMPT CONFIGURATION WITH SOURCES:")
        logging.info(f"   {json.dumps(all_prompts_with_source, indent=4)}")
        logging.info(f"   {'='*60}")
        
        cli_overrides = [field for field, info in all_prompts_with_source.items() if info.get("source") == "cli_override"]
        if cli_overrides:
            logging.info(f"📝 CLI overrides detected: {', '.join(cli_overrides)}")
            logging.info(f"🎯 Total CLI overrides: {len(cli_overrides)}")
        else:
            logging.info(f"📝 No CLI overrides, using profile/system defaults")
    
    # Store the complete source information for later use
    prompt_config['_source_info'] = all_prompts_with_source
    
    return prompt_config

def _get_cli_profile_prompt_value(field: str) -> Any:
    """
    Get prompt value from CLI profile configuration.
    
    Args:
        field: Prompt field name
        
    Returns:
        Any: Prompt value from CLI profile, or None if not found
    """
    try:
        import config.config_base as config_base
        
        # Map field names to config_base attributes
        field_mapping = {
            'system_prompt': 'SYSTEM_PROMPT',
            'user_prompt': 'USER_PROMPT',
            'json_format_instructions': 'JSON_FORMAT_INSTRUCTIONS',
            'mandatory_keys': 'MANDATORY_KEYS',
            'text_first_regex_criteria': 'TEXT_FIRST_REGEX_CRITERIA'
        }
        
        if field in field_mapping:
            config_attr = field_mapping[field]
            if hasattr(config_base, config_attr):
                return getattr(config_base, config_attr)
        
        return None
    except Exception as e:
        logging.debug(f"Could not get CLI profile prompt value for {field}: {e}")
        return None

def _get_test_profile_prompt_value(field: str, test_profile: str) -> Any:
    """
    Get prompt value from test profile configuration.
    
    Args:
        field: Prompt field name
        test_profile: Test profile name
        
    Returns:
        Any: Test profile prompt value, or None if not found
    """
    try:
        import importlib.util
        
        # Load prompt configuration from test profile
        cli_test_path = Path(__file__).parent.parent / "Ultra_Arena_Main_CLI_Test"
        prompt_config_path = cli_test_path / "test_fixtures" / test_profile / "fixture_prompts_config.py"
        
        if prompt_config_path.exists():
            spec = importlib.util.spec_from_file_location("fixture_prompts_config", str(prompt_config_path))
            if spec and spec.loader:
                fixture_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(fixture_module)
                
                # Map field names to fixture variables
                field_mapping = {
                    'system_prompt': 'SYSTEM_PROMPT',
                    'user_prompt': 'USER_PROMPT',
                    'json_format_instructions': 'JSON_FORMAT_INSTRUCTIONS',
                    'mandatory_keys': 'MANDATORY_KEYS',
                    'text_first_regex_criteria': 'TEXT_FIRST_REGEX_CRITERIA'
                }
                
                if field in field_mapping:
                    fixture_attr = field_mapping[field]
                    if hasattr(fixture_module, fixture_attr):
                        return getattr(fixture_module, fixture_attr)
        
        return None
    except Exception as e:
        logging.debug(f"Could not get test profile prompt value for {field}: {e}")
        return None

def _get_system_prompt_value(field: str) -> Any:
    """
    Get prompt value from system defaults.
    
    Args:
        field: Prompt field name
        
    Returns:
        Any: System default prompt value, or None if not found
    """
    try:
        # System defaults (hardcoded fallbacks)
        system_defaults = {
            'system_prompt': "You are a specialized AI assistant for data extraction and analysis.",
            'user_prompt': "Please extract the requested information from the provided documents.",
            'json_format_instructions': "Return the extracted data in valid JSON format.",
            'mandatory_keys': ["INVOICE_NO", "TOTAL_AMOUNT", "INVOICE_ISSUE_DATE"],
            'text_first_regex_criteria': r"invoice|receipt|bill"
        }
        
        return system_defaults.get(field)
    except Exception as e:
        logging.debug(f"Could not get system prompt value for {field}: {e}")
        return None

def _inject_prompt_overrides(prompt_config: dict) -> None:
    """
    Inject prompt configuration into config_base with source tracking.
    
    Args:
        prompt_config: Dictionary containing prompt configuration with source information
    """
    try:
        import config.config_base as config_base
        import json
        
        logging.info(f"🎯 INJECTING PROMPT CONFIGURATION:")
        logging.info(f"   {'='*60}")
        
        # Get source information if available
        source_info = prompt_config.get('_source_info', {})
        
        if source_info:
            logging.info(f"📄 PROMPT CONFIGURATION BEING INJECTED:")
            logging.info(f"   {json.dumps(source_info, indent=4)}")
            logging.info(f"   {'='*60}")
            
            # Inject each prompt with its source
            for field, info in source_info.items():
                if field != '_source_info' and 'value' in info:
                    value = info['value']
                    source = info['source']
                    
                    # Map field names to config_base attributes
                    field_mapping = {
                        'system_prompt': 'SYSTEM_PROMPT',
                        'user_prompt': 'USER_PROMPT',
                        'json_format_instructions': 'JSON_FORMAT_INSTRUCTIONS',
                        'mandatory_keys': 'MANDATORY_KEYS',
                        'text_first_regex_criteria': 'TEXT_FIRST_REGEX_CRITERIA'
                    }
                    
                    if field in field_mapping:
                        config_attr = field_mapping[field]
                        setattr(config_base, config_attr, value)
                        logging.debug(f"✅ Injected {field} ({source}): {str(value)[:100]}...")
        else:
            # Fallback to old method for backward compatibility
            logging.info(f"📄 PROMPT OVERRIDES BEING INJECTED (legacy mode):")
            prompts_with_source = {}
            for key, value in prompt_config.items():
                if key != '_source_info':
                    prompts_with_source[key] = {
                        "value": value,
                        "source": "cli_override"
                    }
            logging.info(f"   {json.dumps(prompts_with_source, indent=4)}")
            logging.info(f"   {'='*60}")
            
            if 'system_prompt' in prompt_config:
                config_base.SYSTEM_PROMPT = prompt_config['system_prompt']
            if 'user_prompt' in prompt_config:
                config_base.USER_PROMPT = prompt_config['user_prompt']
            if 'json_format_instructions' in prompt_config:
                config_base.JSON_FORMAT_INSTRUCTIONS = prompt_config['json_format_instructions']
            if 'mandatory_keys' in prompt_config:
                config_base.MANDATORY_KEYS = prompt_config['mandatory_keys']
            if 'text_first_regex_criteria' in prompt_config:
                config_base.TEXT_FIRST_REGEX_CRITERIA = prompt_config['text_first_regex_criteria']
        
        logging.info(f"🎉 All prompt configuration injected successfully!")
            
    except Exception as e:
        logging.error(f"❌ Failed to inject CLI prompt overrides: {e}")
        raise

def _load_test_profile_prompt_config(test_profile: str) -> None:
    """
    Load prompt configuration from test profile and inject into config_base.
    Test profile prompts have higher priority than CLI profile prompts.
    
    Args:
        test_profile: Name of the test profile to load
    """
    try:
        import config.config_base as config_base
        import importlib.util
        
        # Load prompt configuration from test profile
        cli_test_path = Path(__file__).parent.parent / "Ultra_Arena_Main_CLI_Test"
        prompt_config_path = cli_test_path / "test_fixtures" / test_profile / "fixture_prompts_config.py"
        
        if prompt_config_path.exists():
            spec = importlib.util.spec_from_file_location("fixture_prompts_config", str(prompt_config_path))
            if spec and spec.loader:
                prompt_config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(prompt_config_module)
                
                # Inject prompt configuration into config_base (overriding CLI profile prompts)
                if hasattr(prompt_config_module, 'SYSTEM_PROMPT'):
                    config_base.SYSTEM_PROMPT = prompt_config_module.SYSTEM_PROMPT
                    logging.info(f"📝 Loaded test profile SYSTEM_PROMPT from: {test_profile}")
                if hasattr(prompt_config_module, 'USER_PROMPT'):
                    config_base.USER_PROMPT = prompt_config_module.USER_PROMPT
                    logging.info(f"📝 Loaded test profile USER_PROMPT from: {test_profile}")
                if hasattr(prompt_config_module, 'JSON_FORMAT_INSTRUCTIONS'):
                    config_base.JSON_FORMAT_INSTRUCTIONS = prompt_config_module.JSON_FORMAT_INSTRUCTIONS
                    logging.info(f"📝 Loaded test profile JSON_FORMAT_INSTRUCTIONS from: {test_profile}")
                if hasattr(prompt_config_module, 'MANDATORY_KEYS'):
                    config_base.MANDATORY_KEYS = prompt_config_module.MANDATORY_KEYS
                    logging.info(f"📝 Loaded test profile MANDATORY_KEYS from: {test_profile}")
                if hasattr(prompt_config_module, 'TEXT_FIRST_REGEX_CRITERIA'):
                    config_base.TEXT_FIRST_REGEX_CRITERIA = prompt_config_module.TEXT_FIRST_REGEX_CRITERIA
                    logging.info(f"📝 Loaded test profile TEXT_FIRST_REGEX_CRITERIA from: {test_profile}")
            else:
                logging.warning(f"⚠️ Could not load test profile prompt config from: {prompt_config_path}")
        else:
            logging.warning(f"⚠️ Test profile prompt config file not found: {prompt_config_path}")
            
    except Exception as e:
        logging.error(f"❌ Failed to load test profile prompt configuration: {e}")
        raise

def main():
    """Main CLI function with performance monitoring."""
    
    try:
        # Time argument parsing
        with time_operation("argument_parsing", "cli_setup"):
            parser = argparse.ArgumentParser(description="Ultra Arena Main CLI")
            
            parser.add_argument(
                "--profile", 
                type=str,
                default="default_profile_base",
                help="Profile to use"
            )
            
            parser.add_argument(
                "--test-profile", 
                type=str,
                help="Test profile to use"
            )
            
            parser.add_argument(
                "--combo-name", 
                type=str,
                help="Combo name to use"
            )
            
            parser.add_argument(
                "--input", 
                type=str,
                help="Input directory path"
            )
            
            parser.add_argument(
                "--benchmark-eval-mode", 
                action="store_true",
                help="Enable benchmark evaluation mode"
            )
            
            parser.add_argument(
                "--benchmark-file", 
                type=str,
                help="Benchmark file path"
            )
            
            parser.add_argument(
                "--streaming", 
                action="store_true",
                help="Enable streaming"
            )
            
            parser.add_argument(
                "--max-cc-strategies", 
                type=str,
                default="1",
                help="Max concurrent strategies (or 'max' for all cores)"
            )
            
            parser.add_argument(
                "--max-cc-filegroups", 
                type=int,
                default=1,
                help="Max concurrent file groups"
            )
            
            parser.add_argument(
                "--max-files-per-request", 
                type=int,
                help="Max files per request"
            )
            
            parser.add_argument(
                "--verbose", 
                action="store_true",
                help="Enable verbose logging"
            )
            
            # Prompt configuration arguments
            parser.add_argument(
                "--system-prompt", 
                type=str,
                help="Override system prompt"
            )
            
            parser.add_argument(
                "--user-prompt", 
                type=str,
                help="Override user prompt"
            )
            
            parser.add_argument(
                "--json-format-instructions", 
                type=str,
                help="Override JSON format instructions"
            )
            
            parser.add_argument(
                "--mandatory-keys", 
                type=str,
                nargs='+',
                help="Override mandatory keys (space-separated list)"
            )
            
            parser.add_argument(
                "--text-first-regex-criteria", 
                type=str,
                help="Override text first regex criteria (JSON string)"
            )
            
            args = parser.parse_args()
        
        # Time logging setup
        with time_operation("logging_setup", "cli_setup"):
            setup_logging(verbose=args.verbose)
        
        # Time concurrency configuration
        with time_operation("concurrency_configuration", "cli_setup"):
            if args.max_cc_strategies.lower() == 'max':
                import multiprocessing
                max_cc_strategies = multiprocessing.cpu_count()
                logging.info(f"🖥️ Using max concurrent strategies: {max_cc_strategies}")
            else:
                try:
                    max_cc_strategies = int(args.max_cc_strategies)
                except ValueError:
                    logging.error(f"Invalid max-cc-strategies value: {args.max_cc_strategies}")
                    return 1
        
        # Time profile injection
        with time_operation("profile_injection", "cli_setup"):
            inject_profile_config(args.profile)
            
            # Load CLI prompt configuration
            _load_cli_prompt_config()
            
            # Handle prompt overrides from command line arguments
            prompt_overrides = {}
            if args.system_prompt:
                prompt_overrides['system_prompt'] = args.system_prompt
            if args.user_prompt:
                prompt_overrides['user_prompt'] = args.user_prompt
            if args.json_format_instructions:
                prompt_overrides['json_format_instructions'] = args.json_format_instructions
            if args.mandatory_keys:
                prompt_overrides['mandatory_keys'] = args.mandatory_keys
            if args.text_first_regex_criteria:
                import json
                try:
                    prompt_overrides['text_first_regex_criteria'] = json.loads(args.text_first_regex_criteria)
                except json.JSONDecodeError:
                    logging.error(f"❌ Invalid JSON format for --text-first-regex-criteria: {args.text_first_regex_criteria}")
                    return 1
            
            # Resolve prompt configuration with source tracking
            resolved_prompt_config = _resolve_prompt_config_with_sources(prompt_overrides, args.test_profile)
            
            # Inject the resolved prompt configuration
            _inject_prompt_overrides(resolved_prompt_config)
        
        # Time benchmark mode setup
        with time_operation("benchmark_mode_setup", "cli_setup"):
            benchmark_file_path = None
            
            if args.benchmark_eval_mode:
                # Benchmark evaluation mode enabled
                if not args.benchmark_file:
                    logging.error(f"❌ --benchmark-file is required when --benchmark-eval-mode is used")
                    return 1
                
                benchmark_file_path = Path(args.benchmark_file)
                logging.info(f"🔍 Benchmark evaluation mode enabled")
                
                if not benchmark_file_path.exists():
                    logging.error(f"❌ Benchmark file does not exist: {benchmark_file_path}")
                    return 1
            else:
                # Normal mode
                if args.benchmark_file:
                    logging.warning(f"⚠️ --benchmark-file provided but --benchmark-eval-mode not used - ignoring benchmark file")
                
                logging.info(f"📊 Normal mode - using zero accuracy values")
        
        # Time test profile handling
        with time_operation("test_profile_handling", "cli_setup"):
            input_pdf_dir_path = None
            output_dir = None
            
            if args.test_profile:
                try:
                    # Import from CLI_Test directory
                    cli_test_path = Path(__file__).parent.parent / "Ultra_Arena_Main_CLI_Test"
                    sys.path.insert(0, str(cli_test_path))
                    from test_config import get_test_profile_paths
                    test_paths = get_test_profile_paths(args.test_profile)
                    input_pdf_dir_path = Path(test_paths['input_pdf_dir_path'])
                    output_dir = str(test_paths['output_dir'])
                    
                    # Load test profile prompt configuration (higher priority than CLI profile)
                    _load_test_profile_prompt_config(args.test_profile)
                    
                    # If benchmark evaluation mode is enabled but no benchmark file specified, use test profile's benchmark file
                    if args.benchmark_eval_mode and not args.benchmark_file and Path(test_paths['benchmark_file_path']).exists():
                        benchmark_file_path = Path(test_paths['benchmark_file_path'])
                        logging.info(f"🔍 Using test profile benchmark file for evaluation mode")
                    
                    logging.info(f"📁 Using test profile: {args.test_profile}")
                    logging.info(f"   Input: {input_pdf_dir_path}")
                    logging.info(f"   Output: {output_dir}")
                    if benchmark_file_path:
                        logging.info(f"   Benchmark: {benchmark_file_path}")
                        
                except ImportError as e:
                    logging.error(f"❌ Test profile '{args.test_profile}' not found: {e}")
                    return 1
            elif args.input:
                # Use provided input path
                input_pdf_dir_path = Path(args.input)
        
        # Time path validation
        with time_operation("path_validation", "cli_setup"):
            if input_pdf_dir_path and not input_pdf_dir_path.exists():
                logging.error(f"❌ Input directory does not exist: {input_pdf_dir_path}")
                return 1
        
        # Time main library processing
        with time_operation("main_processing", "main_processing"):
            # Check if combo mode is requested
            if args.combo_name:
                logging.info(f"🔄 Running combo mode with profile: {args.profile}, combo: {args.combo_name}")
                
                result = run_combo_processing(
                    benchmark_eval_mode=args.benchmark_eval_mode,
                    combo_name=args.combo_name,
                    streaming=args.streaming,
                    max_cc_strategies=max_cc_strategies,
                    max_cc_filegroups=args.max_cc_filegroups,
                    max_files_per_request=args.max_files_per_request,
                    input_pdf_dir_path=input_pdf_dir_path,
                    pdf_file_paths=[],
                    output_dir=output_dir,
                    benchmark_file_path=benchmark_file_path
                )
            else:
                # Use unified processing with default parameter group
                logging.info(f"🔄 Running unified processing with profile: {args.profile}, using default parameter group")
                
                result = run_combo_processing(
                    benchmark_eval_mode=args.benchmark_eval_mode,
                    combo_name=None,  # Will use DEFAULT_STRATEGY_PARAM_GRP
                    streaming=args.streaming,
                    max_cc_strategies=max_cc_strategies,
                    max_cc_filegroups=args.max_cc_filegroups,
                    max_files_per_request=args.max_files_per_request,
                    input_pdf_dir_path=input_pdf_dir_path,
                    pdf_file_paths=[],
                    output_dir=output_dir,
                    benchmark_file_path=benchmark_file_path
                )
        
        return result
        
    except Exception as e:
        logging.error(f"❌ ERROR in CLI execution: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 