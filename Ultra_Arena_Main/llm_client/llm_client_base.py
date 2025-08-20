"""
Base LLM client system supporting multiple providers.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseLLMClient(ABC):
    """Base class for LLM clients."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get("model")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 4000)
        self.timeout = config.get("timeout", 60)
    
    @abstractmethod
    def call_llm(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str, 
                 strategy_type: Optional[str] = None) -> Dict[str, Any]:
        """Call the LLM with user prompt, optional system prompt, and optional files."""
        pass
    
    @abstractmethod
    async def call_llm_async(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str,
                           strategy_type: Optional[str] = None) -> Dict[str, Any]:
        """Call the LLM asynchronously with user prompt, optional system prompt, and optional files."""
        pass
    
 