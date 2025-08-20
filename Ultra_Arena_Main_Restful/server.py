#!/usr/bin/env python3
"""
RESTful API Server for Ultra Arena Main

This module provides a REST API interface to the Ultra_Arena_Main library.
It exposes endpoints for file processing and combo operations.

The server is organized into modular components:
- ConfigManager: Handles configuration management
- RequestValidator: Handles request validation
- RequestProcessor: Handles request processing
"""

import sys
import os
import logging
import time
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps

# Add the Ultra_Arena_Main to the Python path
ultra_arena_main_path = Path(__file__).parent.parent / "Ultra_Arena_Main"
sys.path.insert(0, str(ultra_arena_main_path))

# Import the main functions from Ultra_Arena_Main
from main_modular import setup_logging

# Import our modular components
from server_utils.config_manager import ConfigManager
from server_utils.request_validator import RequestValidator
from server_utils.request_processor import RequestProcessor

# Setup Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup logging
setup_logging(verbose=True)
logger = logging.getLogger(__name__)

# Get server configuration from environment
RUN_PROFILE = os.environ.get('RUN_PROFILE', 'default_profile_restful')
logger.info(f"Server configured to use profile: {RUN_PROFILE}")

# Initialize modular components
config_manager = ConfigManager(RUN_PROFILE)
request_processor = RequestProcessor(config_manager)


# =============================================================================
# PERFORMANCE MONITORING
# =============================================================================

# Import the new performance monitoring system
from performance_measure import (
    start_monitoring,
    end_monitoring,
    time_operation,
    mark_point,
    track_memory
)


# =============================================================================
# HEALTH CHECK ENDPOINT
# =============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Ultra Arena Main RESTful API",
        "version": "1.0.0"
    })


# =============================================================================
# PROCESSING ENDPOINTS
# =============================================================================


@app.route('/api/process/combo', methods=['POST'])
def process_combo():
    """
    Enhanced combo processing with consistent parameter naming and strict validation.
    
    Expected JSON payload (flattened structure):
    {
        "combo_name": "combo_test_10_strategies",  // Required
        "input_pdf_dir_path": "/path/to/input",  // Required
        "output_dir": "/path/to/output",  // Required
        "run_type": "normal",  // optional, defaults to "normal"
        "streaming": false,  // optional, defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 3,  // optional, defaults to config DEFAULT_MAX_CC_STRATEGIES
        "max_cc_filegroups": 5,  // optional, defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 10  // optional, defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    For evaluation runs:
    {
        "combo_name": "combo_test_10_strategies",  // Required
        "input_pdf_dir_path": "/path/to/input",  // Required
        "output_dir": "/path/to/output",  // Required
        "run_type": "evaluation",  // optional, defaults to "normal"
        "benchmark_file_path": "/path/to/benchmark.xlsx"  // Required for evaluation mode
    }
    
    Note: Defaults can be overridden in profile_config.py
    """
    # Start performance monitoring
    monitor = start_monitoring("REST_API_Process_Combo")
    track_memory("request_start")
    
    try:
        logger.info(f"🚀 STARTING /api/process/combo request")
        
        with time_operation("http_request_parsing", "http_request_parsing"):
            data = request.get_json()
            is_valid, error_msg = RequestValidator.validate_json_request(data)
            if not is_valid:
                return jsonify({"error": error_msg}), 400
        
        track_memory("after_request_parsing")
        
        with time_operation("configuration_setup", "configuration_setup"):
            try:
                config = request_processor.create_unified_request_config(data, use_default_combo=False)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        
        track_memory("after_config_setup")
        
        with time_operation("main_library_processing", "main_library_processing"):
            result_code = request_processor.execute_processing(config)
        
        track_memory("after_main_processing")
        
        with time_operation("response_formatting", "response_formatting"):
            response = request_processor.format_combo_response(result_code, config)
        
        track_memory("request_end")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ ERROR in /api/process/combo endpoint: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        end_monitoring()


# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@app.route('/api/combos', methods=['GET'])
def get_combos():
    """
    Endpoint 3.1.3: GET API that exposes available combos
    """
    # Start performance monitoring
    monitor = start_monitoring("REST_API_Get_Combos")
    track_memory("request_start")
    
    try:
        logger.info(f"🚀 STARTING /api/combos request")
        
        with time_operation("combo_retrieval", "combo_retrieval"):
            logger.info(f"Getting available combos for profile: {RUN_PROFILE}")
            combos = config_manager.get_available_combos()
        
        track_memory("after_combo_retrieval")
        
        with time_operation("response_formatting", "response_formatting"):
            response = jsonify({
                "status": "success",
                "combos": combos,
                "count": len(combos)
            })
        
        track_memory("request_end")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ ERROR in /api/combos endpoint: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        end_monitoring()


# =============================================================================
# SERVER STARTUP
# =============================================================================

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5002))
    
    logger.info(f"Starting Ultra Arena Main RESTful API server on port {port}")
    logger.info(f"Using profile: {RUN_PROFILE}")
    logger.info("Available endpoints:")
    logger.info("  GET  /health - Health check")
    logger.info("  POST /api/process/combo - Process combo")
    logger.info("  GET  /api/combos - Get available combos")
    
    # Configure Flask for production use (no debug mode to prevent timeouts)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True) 