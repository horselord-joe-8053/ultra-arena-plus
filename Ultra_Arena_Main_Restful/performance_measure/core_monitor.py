#!/usr/bin/env python3
"""
Core Performance Monitor for REST API

This module provides a clean, simple performance monitoring system that focuses
on measuring the key time-consuming parts of REST API request processing.
"""

import time
import logging
import json
import os
from pathlib import Path
from contextlib import contextmanager
from typing import Dict, Any, Optional

# Global monitor instance
_monitor = None

class PerformanceMonitor:
    """Simple performance monitor focusing on key REST API execution phases."""
    
    def __init__(self, operation_name: str = "REST_API_Request"):
        self.operation_name = operation_name
        self.start_time = time.time()
        self.logger = logging.getLogger(__name__)
        
        # Key performance categories for REST API
        self.timings = {
            "http_request_parsing": 0.0,
            "configuration_setup": 0.0,
            "main_library_processing": 0.0,
            "response_formatting": 0.0,
            "total_request_time": 0.0
        }
        
        # Performance markers
        self.markers = {}
        
        # Memory tracking
        self.memory_snapshots = []
        
    def mark(self, name: str, description: str = ""):
        """Mark a specific point in time."""
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.markers[name] = {
            "time": current_time,
            "elapsed": elapsed,
            "description": description
        }
        self.logger.info(f"⏱️  MARK: {name} at {elapsed:.3f}s - {description}")
    
    @contextmanager
    def time_operation(self, operation_name: str, category: str):
        """Time an operation and add it to the specified category."""
        start_time = time.time()
        self.logger.info(f"⏱️  START: {operation_name}")
        
        try:
            yield
        finally:
            end_time = time.time()
            duration = end_time - start_time
            self.timings[category] += duration
            self.logger.info(f"⏱️  END: {operation_name} - Duration: {duration:.3f}s")
    
    def track_memory(self, operation: str = "memory_snapshot"):
        """Track memory usage."""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            snapshot = {
                "operation": operation,
                "timestamp": time.time(),
                "rss_mb": memory_info.rss / 1024 / 1024,
                "vms_mb": memory_info.vms / 1024 / 1024
            }
            self.memory_snapshots.append(snapshot)
            self.logger.info(f"💾 MEMORY: {operation} - RSS: {snapshot['rss_mb']:.1f}MB")
        except ImportError:
            self.logger.warning("psutil not available for memory tracking")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a clean performance summary."""
        total_time = time.time() - self.start_time
        
        # Calculate percentages
        summary = {
            "operation_name": self.operation_name,
            "total_time": total_time,
            "breakdown": {},
            "memory_usage": {},
            "markers": self.markers
        }
        
        # Add breakdown with percentages
        for category, duration in self.timings.items():
            percentage = (duration / total_time) * 100 if total_time > 0 else 0
            summary["breakdown"][category] = {
                "duration": duration,
                "percentage": percentage
            }
        
        # Add memory usage summary
        if self.memory_snapshots:
            latest = self.memory_snapshots[-1]
            summary["memory_usage"] = {
                "final_rss_mb": latest["rss_mb"],
                "final_vms_mb": latest["vms_mb"],
                "snapshots_count": len(self.memory_snapshots)
            }
        
        return summary
    
    def log_summary(self):
        """Log a formatted performance summary."""
        summary = self.get_summary()
        
        self.logger.info(f"📊 PERFORMANCE SUMMARY for {summary['operation_name']}:")
        self.logger.info("=" * 60)
        
        for category, data in summary["breakdown"].items():
            self.logger.info(f"  {category}: {data['duration']:.3f}s ({data['percentage']:.1f}%)")
        
        self.logger.info(f"  TOTAL: {summary['total_time']:.3f}s")
        
        if summary["memory_usage"]:
            self.logger.info(f"  MEMORY: {summary['memory_usage']['final_rss_mb']:.1f}MB RSS")
        
        self.logger.info("=" * 60)
    
    def save_summary(self, filename: Optional[str] = None):
        """Save performance summary to JSON file."""
        # Create results directory
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = int(time.time())
            filename = f"rest_performance_summary_{timestamp}.json"
        
        filepath = results_dir / filename
        
        # Save summary
        with open(filepath, 'w') as f:
            json.dump(self.get_summary(), f, indent=2)
        
        self.logger.info(f"💾 Performance summary saved to: {filepath}")
        return str(filepath)

# Global helper functions
def start_monitoring(operation_name: str = "REST_API_Request") -> PerformanceMonitor:
    """Start a new performance monitoring session."""
    global _monitor
    _monitor = PerformanceMonitor(operation_name)
    return _monitor

def end_monitoring() -> Dict[str, Any]:
    """End the current monitoring session and return summary."""
    global _monitor
    if _monitor:
        summary = _monitor.get_summary()
        _monitor.log_summary()
        _monitor.save_summary()
        _monitor = None
        return summary
    return {}

@contextmanager
def time_operation(operation_name: str, category: str):
    """Global context manager for timing operations."""
    global _monitor
    if not _monitor:
        _monitor = start_monitoring()
    
    with _monitor.time_operation(operation_name, category):
        yield

def mark_point(name: str, description: str = ""):
    """Global function to mark a performance point."""
    global _monitor
    if not _monitor:
        _monitor = start_monitoring()
    
    _monitor.mark(name, description)

def track_memory(operation: str = "memory_snapshot"):
    """Global function to track memory usage."""
    global _monitor
    if not _monitor:
        _monitor = start_monitoring()
    
    _monitor.track_memory(operation)
