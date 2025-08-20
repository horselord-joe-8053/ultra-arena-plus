"""
Grok-specific mixin for OpenAI-style clients.

This mixin provides Grok-specific functionality while inheriting common
functionality from BaseClientMixin.
"""

import logging
from typing import Dict, Any

from .base_client_mixin import BaseClientMixin


class GrokMixin(BaseClientMixin):
    """Grok-specific functionality."""
    
    provider_name = "Grok"
    
    def _create_client(self, api_key: str):
        """Create Grok client using OpenAI-compatible API with x.ai base URL."""
        try:
            from openai import OpenAI
            return OpenAI(
                api_key=api_key,
                base_url="https://api.x.ai/v1"
            )
        except ImportError:
            raise ImportError("OpenAI library not available. Install with: pip install openai")
    
    def _create_completion_request(self, messages: list, **kwargs) -> Any:
        """Create Grok completion request."""
        return self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
            **kwargs
        ) 