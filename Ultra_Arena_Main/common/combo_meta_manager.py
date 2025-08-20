#!/usr/bin/env python3
"""
Combo Meta File Manager for Ultra Arena

This module handles creation of combo_meta.json files and manages the new
timestamped directory structure for results.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from .request_id_generator import RequestIDGenerator

logger = logging.getLogger(__name__)


class ComboMetaManager:
    """Manages combo meta files and directory structure."""
    
    @staticmethod
    def create_results_directory(output_base_dir: str, request_id: str) -> Path:
        """
        Create the new timestamped results directory.
        
        Args:
            output_base_dir: Base output directory
            request_id: Unique request ID
            
        Returns:
            Path: Path to the created results directory
        """
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
        results_dir = Path(f"{output_base_dir}/results_{timestamp}_{request_id}")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 Created results directory: {results_dir}")
        return results_dir
    
    @staticmethod
    def create_combo_meta_file(results_dir: Path, request_metadata: Dict[str, Any], 
                              combo_name: str, strategy_groups: List[str], 
                              num_files: int) -> Path:
        """
        Create combo_meta.json file with request metadata and strategy information.
        
        Args:
            results_dir: Results directory path
            request_metadata: Request metadata from RequestIDGenerator
            combo_name: Name of the combo being processed
            strategy_groups: List of strategy group names
            num_files: Number of files to process
            
        Returns:
            Path: Path to the created combo_meta.json file
        """
        meta_data = {
            "request_id": request_metadata["request_id"],
            "request_mechanism": request_metadata["request_mechanism"],
            "request_start_time": request_metadata["request_start_time"],
            "utc_timezone": request_metadata["utc_timezone"],
            "num_files_to_process": num_files,
            "combo_name": combo_name,
            "num_strategies": len(strategy_groups),
            "strategy_groups": strategy_groups
        }
        
        meta_file = results_dir / "combo_meta.json"
        with open(meta_file, 'w') as f:
            json.dump(meta_data, f, indent=2)
        
        logger.info(f"📄 Created combo_meta.json: {meta_file}")
        return meta_file
    
    @staticmethod
    def initialize_strategy_files(json_dir: Path, csv_dir: Path, strategy_groups: List[str], param_grps: Dict = None) -> Dict[str, Dict[str, str]]:
        """
        Pre-create detailed JSON and CSV files for all strategies with initial structure.
        
        Args:
            json_dir: JSON directory path
            csv_dir: CSV directory path
            strategy_groups: List of strategy group names
            param_grps: Parameter groups dictionary to get strategy details
            
        Returns:
            Dict[str, Dict[str, str]]: Mapping of strategy group names to their generated filenames (json and csv)
        """
        created_files = {}
        
        # Use a single timestamp for all files to ensure consistency
        from datetime import datetime
        timestamp = datetime.now().strftime("%m-%d-%H-%M-%S")
        
        for strategy_group in strategy_groups:
            # Get strategy parameters from param_grps
            if param_grps and strategy_group in param_grps:
                group_params = param_grps[strategy_group]
                strategy = group_params.get("strategy", "unknown")
                mode = group_params.get("mode", "unknown")
                provider = group_params.get("provider", "unknown")
                model = group_params.get("model", "unknown")
            else:
                # Fallback values if param_grps not available
                strategy = "unknown"
                mode = "unknown"
                provider = "unknown"
                model = "unknown"
            
            # Generate timestamped filenames (same format as actual result files)
            clean_model = model.replace(":", "_").replace("/", "_").replace("-", "_")
            json_filename = f"{strategy}_{mode}_{provider}_{clean_model}_{timestamp}.json"
            csv_filename = f"{strategy}_{mode}_{provider}_{clean_model}_{timestamp}.csv"
            
            json_file = json_dir / json_filename
            csv_file = csv_dir / csv_filename
            
            # Create detailed initial data structure matching actual result files
            initial_data = {
                "run_settings": {
                    "strategy": strategy,
                    "mode": mode,
                    "llm_provider": provider,
                    "llm_model": model
                },
                "file_stats": {},
                "group_stats": {},
                "retry_stats": {
                    "num_files_may_need_retry": 0,
                    "num_files_had_retry": 0,
                    "percentage_files_had_retry": 0.0,
                    "num_file_failed_after_max_retries": 0,
                    "actual_tokens_for_retries": 0,
                    "retry_prompt_tokens": 0,
                    "retry_candidate_tokens": 0,
                    "retry_other_tokens": 0,
                    "retry_total_tokens": 0
                },
                "overall_stats": {
                    "total_files": 0,
                    "total_estimated_tokens": 0,
                    "total_wall_time_in_sec": 0.0,
                    "total_group_wall_time_in_sec": 0.0,
                    "total_prompt_tokens": 0,
                    "total_candidate_tokens": 0,
                    "total_other_tokens": 0,
                    "total_actual_tokens": 0,
                    "average_prompt_tokens_per_file": 0.0,
                    "average_candidate_tokens_per_file": 0.0,
                    "average_other_tokens_per_file": 0.0,
                    "average_total_tokens_per_file": 0.0
                },
                "benchmark_errors": {
                    "total_unmatched_fields": 0,
                    "total_unmatched_files": 0
                },
                "overall_cost": {
                    "price_obtained_date": "",
                    "prompt_token_price_per_1M": 0.0,
                    "candidate_token_price_per_1M": 0.0,
                    "other_token_price_per_1M": 0.0,
                    "total_prompt_token_cost": 0.0,
                    "total_candidate_token_cost": 0.0,
                    "total_other_token_cost": 0.0,
                    "total_token_cost": 0.0
                }
            }
            
            # Create JSON file
            with open(json_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
            
            # Create empty CSV file (will be populated during processing)
            with open(csv_file, 'w') as f:
                f.write("")  # Empty file, will be populated during processing
            
            created_files[strategy_group] = {
                "json": json_filename,
                "csv": csv_filename
            }
            logger.debug(f"📄 Initialized strategy files: {json_file}, {csv_file}")
        
        logger.info(f"📄 Initialized {len(created_files)} strategy file pairs (JSON + CSV)")
        return created_files
    
    @staticmethod
    def create_combo_directories(results_dir: Path) -> tuple[Path, Path]:
        """
        Create csv and json subdirectories within the results directory.
        
        Args:
            results_dir: Results directory path
            
        Returns:
            tuple[Path, Path]: Paths to csv and json directories
        """
        csv_dir = results_dir / "csv"
        json_dir = results_dir / "json"
        
        csv_dir.mkdir(exist_ok=True)
        json_dir.mkdir(exist_ok=True)
        
        logger.debug(f"📁 Created subdirectories: {csv_dir}, {json_dir}")
        return csv_dir, json_dir
