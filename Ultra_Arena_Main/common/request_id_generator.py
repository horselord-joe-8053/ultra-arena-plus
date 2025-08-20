#!/usr/bin/env python3
"""
Thread-safe Request ID Generator for Ultra Arena

This module provides thread-safe UUID generation and request mechanism detection
for tracking processing requests across different entry points.
"""

import uuid
import threading
import time
import inspect
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RequestIDGenerator:
    """Thread-safe request ID generator with mechanism detection."""
    
    _lock = threading.Lock()
    
    @staticmethod
    def generate_request_id() -> str:
        """
        Generate a thread-safe unique request ID.
        
        Returns:
            str: Unique UUID string
        """
        with RequestIDGenerator._lock:
            request_id = str(uuid.uuid4())
            logger.debug(f"🔑 Generated request ID: {request_id}")
            return request_id
    
    @staticmethod
    def detect_request_mechanism() -> str:
        """
        Detect the request mechanism by analyzing the call stack.
        
        Returns:
            str: Request mechanism ('rest', 'cli', 'direct', or 'other')
        """
        try:
            # Get the call stack
            frame = inspect.currentframe()
            stack = []
            while frame:
                stack.append(frame)
                frame = frame.f_back
            
            # Look for characteristic patterns in the call stack
            stack_str = str(stack)
            
            if 'flask' in stack_str.lower() or 'request_processor' in stack_str.lower():
                return 'rest'
            elif 'argparse' in stack_str.lower() or 'main.py' in stack_str.lower():
                return 'cli'
            elif 'direct_test' in stack_str.lower() or 'direct_call' in stack_str.lower():
                return 'direct'
            else:
                return 'other'
                
        except Exception as e:
            logger.warning(f"⚠️ Could not detect request mechanism: {e}")
            return 'other'
    
    @staticmethod
    def get_request_start_time() -> str:
        """
        Get the current request start time in ISO format.
        
        Returns:
            str: ISO formatted timestamp
        """
        return datetime.utcnow().isoformat()
    
    @staticmethod
    def get_utc_timezone() -> str:
        """
        Get UTC timezone identifier.
        
        Returns:
            str: UTC timezone identifier
        """
        return "UTC"
    
    @staticmethod
    def create_request_metadata() -> Dict[str, Any]:
        """
        Create complete request metadata.
        
        Returns:
            Dict[str, Any]: Complete request metadata
        """
        return {
            "request_id": RequestIDGenerator.generate_request_id(),
            "request_mechanism": RequestIDGenerator.detect_request_mechanism(),
            "request_start_time": RequestIDGenerator.get_request_start_time(),
            "utc_timezone": RequestIDGenerator.get_utc_timezone()
        }
