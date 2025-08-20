#!/usr/bin/env python3
"""
Core Performance Monitor

This module provides a clean, simple performance monitoring system that focuses
on measuring the 4-5 key time-consuming parts of CLI execution.
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
    """Simple performance monitor focusing on key execution phases."""
    
    def __init__(self, operation_name: str = "CLI_Execution"):
        self.operation_name = operation_name
        self.start_time = time.time()
        self.logger = logging.getLogger(__name__)
        
        # Key performance categories
        self.timings = {
            "python_startup": 0.0,
            "module_imports": 0.0,
            "cli_setup": 0.0,
            "main_processing": 0.0,
            "file_operations": 0.0
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
        
        # Add memory summary
        if self.memory_snapshots:
            initial = self.memory_snapshots[0]
            final = self.memory_snapshots[-1]
            summary["memory_usage"] = {
                "initial_rss_mb": initial["rss_mb"],
                "final_rss_mb": final["rss_mb"],
                "growth_mb": final["rss_mb"] - initial["rss_mb"]
            }
        
        return summary
    
    def log_summary(self):
        """Log a clean performance summary."""
        summary = self.get_summary()
        
        self.logger.info("=" * 60)
        self.logger.info("📊 PERFORMANCE SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"⏱️  Total Time: {summary['total_time']:.3f}s")
        
        for category, data in summary["breakdown"].items():
            self.logger.info(f"  {category.replace('_', ' ').title()}: {data['duration']:.3f}s ({data['percentage']:.1f}%)")
        
        if summary["memory_usage"]:
            self.logger.info(f"💾 Memory Growth: {summary['memory_usage']['growth_mb']:.1f}MB")
        
        self.logger.info("=" * 60)
    
    def save_summary(self, filename: Optional[str] = None):
        """Save performance summary to JSON file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"performance_summary_{timestamp}.json"
        
        # Ensure results directory exists
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)
        
        filepath = results_dir / filename
        summary = self.get_summary()
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        self.logger.info(f"📄 Performance summary saved to: {filepath}")
        return filepath

# Global functions for easy access
def start_monitoring(operation_name: str = "CLI_Execution") -> PerformanceMonitor:
    """Start performance monitoring."""
    global _monitor
    _monitor = PerformanceMonitor(operation_name)
    _monitor.mark("monitoring_started", "Performance monitoring started")
    return _monitor

def end_monitoring() -> Dict[str, Any]:
    """End performance monitoring and return summary."""
    global _monitor
    if _monitor:
        _monitor.mark("monitoring_ended", "Performance monitoring completed")
        summary = _monitor.get_summary()
        _monitor.log_summary()
        _monitor.save_summary()
        return summary
    return {}

@contextmanager
def time_operation(operation_name: str, category: str):
    """Time an operation using the global monitor."""
    global _monitor
    if _monitor:
        with _monitor.time_operation(operation_name, category):
            yield
    else:
        yield

def mark_point(name: str, description: str = ""):
    """Mark a point using the global monitor."""
    global _monitor
    if _monitor:
        _monitor.mark(name, description)

def track_memory(operation: str = "memory_snapshot"):
    """Track memory using the global monitor."""
    global _monitor
    if _monitor:
        _monitor.track_memory(operation)
