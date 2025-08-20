#!/usr/bin/env python3
"""
Request Validation Module for Ultra Arena RESTful API

This module handles all request validation operations including:
- JSON request validation
- Configuration validation
- Parameter validation
"""

import logging
from pathlib import Path
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)


class RequestValidator:
    """Validates requests for the Ultra Arena RESTful API."""
    
    @staticmethod
    def validate_json_request(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that JSON data is provided.
        
        Args:
            data: The request data to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not data:
            return False, "No JSON data provided"
        return True, None
    
    @staticmethod
    def validate_combo_name(combo_name: str, available_combos: list) -> Tuple[bool, str]:
        """
        Validate that the combo name exists in available combos.
        
        Args:
            combo_name: The combo name to validate
            available_combos: List of available combo names
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not combo_name:
            return False, "combo_name is required"
        
        if combo_name not in available_combos:
            return False, f"Invalid combo_name: '{combo_name}'. Available combos: {available_combos}"
        
        return True, None
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Tuple[bool, str]:
        """
        Validate that all required fields are present and not empty.
        
        Args:
            data: The request data to validate
            required_fields: List of required field names
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        missing_fields = []
        empty_fields = []
        
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
            elif data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                empty_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields: {missing_fields}"
        
        if empty_fields:
            return False, f"Required fields cannot be empty: {empty_fields}"
        
        return True, None
    
    @staticmethod
    def validate_file_paths(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that file paths exist and are accessible.
        
        Args:
            data: The request data containing file paths
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # Validate input directory
        if 'input_pdf_dir_path' in data:
            input_path = Path(data['input_pdf_dir_path'])
            if not input_path.exists():
                return False, f"Input directory does not exist: {input_path}"
            if not input_path.is_dir():
                return False, f"Input path is not a directory: {input_path}"
        
        # Validate benchmark file (if provided)
        if 'benchmark_file_path' in data and data['benchmark_file_path']:
            benchmark_path = Path(data['benchmark_file_path'])
            if not benchmark_path.exists():
                return False, f"Benchmark file does not exist: {benchmark_path}"
            if not benchmark_path.is_file():
                return False, f"Benchmark path is not a file: {benchmark_path}"
        
        return True, None
    
    @staticmethod
    def resolve_run_config(request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve run configuration with intelligent defaults and consistent naming.
        
        Args:
            request_data: The request data to resolve
            
        Returns:
            Dict[str, Any]: Resolved configuration
            
        Raises:
            ValueError: If validation fails
        """
        # Base defaults
        defaults = {
            "run_type": "normal",  # Default to normal mode
            "benchmark_eval_mode": False
        }
        
        # Merge with provided values (flattened structure)
        resolved_config = {**defaults, **request_data}
        
        # Validate required fields
        required_fields = ["input_pdf_dir_path", "output_dir"]
        missing_fields = [field for field in required_fields if not resolved_config.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Set benchmark flags based on benchmark_eval_mode
        if resolved_config["benchmark_eval_mode"]:
            # Evaluation mode enabled
            logger.info("🔍 Benchmark evaluation mode enabled")
            
            # Require benchmark_file_path for evaluation mode
            if not resolved_config.get('benchmark_file_path'):
                raise ValueError("benchmark_file_path is required when benchmark_eval_mode=true")
        else:
            # Normal mode
            logger.info("📊 Normal mode - using zero accuracy values")
        
        return resolved_config
    
    @staticmethod
    def validate_run_config(run_config: Dict[str, Any]) -> bool:
        """
        Validate run configuration based on benchmark presence.
        
        Args:
            run_config: The run configuration dictionary
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        # Always require input_pdf_dir_path and output_dir
        required_fields = ["input_pdf_dir_path", "output_dir"]
        
        # If benchmark_file_path is provided, also require it
        if run_config.get('benchmark_file_path'):
            required_fields.append("benchmark_file_path")
        
        # Check required fields
        missing_fields = [field for field in required_fields if not run_config.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Validate file paths exist
        if "input_pdf_dir_path" in run_config:
            input_path = Path(run_config["input_pdf_dir_path"])
            if not input_path.exists():
                raise ValueError(f"Input directory does not exist: {input_path}")
        
        if "benchmark_file_path" in run_config:
            benchmark_path = Path(run_config["benchmark_file_path"])
            if not benchmark_path.exists():
                raise ValueError(f"Benchmark file does not exist: {benchmark_path}")
        
        return True
