#!/usr/bin/env python3
"""
Configuration Management Module for Ultra Arena RESTful API

This module provides a simplified interface to the optimized configuration assembly system.
It maintains backward compatibility while using the new assemblers for better performance.
"""

import logging
from typing import Dict, Any, List

from .config_assemblers import RestServerConfigAssembler, RequestConfigAssembler, ConfigAssemblyResult

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration for the Ultra Arena RESTful API using optimized assemblers."""
    
    def __init__(self, run_profile: str = 'default_profile_restful'):
        """
        Initialize the configuration manager.
        
        Args:
            run_profile (str): The profile name to use for configuration
        """
        self.run_profile = run_profile
        
        # Initialize the server config assembler
        self._server_assembler = RestServerConfigAssembler(run_profile)
        self._server_config = None
        self._request_assembler = None
        
        # Assemble server configuration at initialization
        self._assemble_server_config()
    
    def _assemble_server_config(self) -> None:
        """Assemble server configuration once at initialization."""
        try:
            logger.info(f"🔧 Initializing server configuration for profile: {self.run_profile}")
            self._server_config = self._server_assembler.assemble_config()
            self._request_assembler = RequestConfigAssembler(self._server_config)
            
            # Inject into config_base for backward compatibility
            self._server_assembler.inject_into_config_base()
            
            logger.info(f"✅ Server configuration initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize server configuration: {e}")
            raise
    
    def get_server_config(self):
        """
        Get the assembled server configuration.
        
        Returns:
            ServerConfig: The assembled server configuration
        """
        return self._server_config
    
    def get_request_assembler(self):
        """
        Get the request config assembler.
        
        Returns:
            RequestConfigAssembler: The request config assembler
        """
        return self._request_assembler
    
    def assemble_request_config(self, request_data: Dict[str, Any], use_default_combo: bool = False) -> ConfigAssemblyResult:
        """
        Assemble request configuration using the optimized assembler.
        
        Args:
            request_data (Dict[str, Any]): Request data from the endpoint
            use_default_combo (bool): If True, use default combo
            
        Returns:
            ConfigAssemblyResult: Assembled configuration with metadata
        """
        if self._request_assembler is None:
            raise RuntimeError("Request assembler not initialized")
        
        return self._request_assembler.assemble_request_config(request_data, use_default_combo)
    
    def inject_profile_config(self) -> None:
        """
        Inject the assembled profile configuration into the Ultra_Arena_Main library.
        
        This method is maintained for backward compatibility but now uses the optimized assembler.
        """
        try:
            if self._server_config is None:
                raise RuntimeError("Server configuration not initialized")
            
            # The configuration is already injected during initialization
            # This method is kept for backward compatibility
            logger.info(f"✅ Profile configuration already injected (using optimized assembler)")
            
        except Exception as e:
            logger.error(f"❌ Failed to inject profile configuration: {e}")
            raise
    
    def get_config_defaults(self) -> Dict[str, Any]:
        """
        Get configuration defaults from the assembled server configuration.
        
        Returns:
            dict: Configuration defaults
        """
        if self._server_config is None:
            raise RuntimeError("Server configuration not initialized")
        
        processing = self._server_config.processing
        return {
            "streaming": processing.streaming,
            "max_cc_strategies": processing.max_cc_strategies,
            "max_cc_filegroups": processing.max_cc_filegroups,
            "max_files_per_request": processing.max_files_per_request
        }
    
    def get_default_combo_name(self) -> str:
        """
        Get the default combo name from the assembled server configuration.
        
        Returns:
            str: The default combo name
        """
        if self._server_config is None:
            raise RuntimeError("Server configuration not initialized")
        
        return self._server_config.default_combo_name
    
    def get_available_combos(self) -> List[str]:
        """
        Get available combos from the assembled server configuration.
        
        Returns:
            List[str]: List of available combo names
        """
        if self._server_config is None:
            raise RuntimeError("Server configuration not initialized")
        
        return self._server_config.available_combos
    
    def get_assembly_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for configuration assembly.
        
        Returns:
            Dict[str, Any]: Performance statistics
        """
        if self._server_config is None:
            return {"error": "Server configuration not initialized"}
        
        return {
            "server_assembly_time_ms": self._server_assembler.get_assembly_time_ms(),
            "server_config_cached": self._server_assembler.is_cached(),
            "profile": self.run_profile
        }
    
    def clear_cache(self) -> None:
        """Clear the server configuration cache."""
        self._server_assembler.clear_cache()
        self._server_config = None
        self._request_assembler = None
        logger.info("🗑️ Configuration cache cleared")
    
    def reload_configuration(self) -> None:
        """Reload the server configuration."""
        logger.info("🔄 Reloading server configuration")
        self.clear_cache()
        self._assemble_server_config()
