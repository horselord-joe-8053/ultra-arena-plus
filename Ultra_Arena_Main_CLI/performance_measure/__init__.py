#!/usr/bin/env python3
"""
Performance Measurement Package

This package provides clean, simple performance monitoring for the Ultra Arena CLI.
It focuses on measuring the 4-5 key time-consuming parts of execution.
"""

from .core_monitor import (
    PerformanceMonitor,
    start_monitoring,
    end_monitoring,
    time_operation,
    mark_point,
    track_memory
)

__all__ = [
    'PerformanceMonitor',
    'start_monitoring', 
    'end_monitoring',
    'time_operation',
    'mark_point',
    'track_memory'
]
