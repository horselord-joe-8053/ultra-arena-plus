"""
OpenAI-specific mixin for OpenAI-style clients.

This mixin provides OpenAI-specific functionality while inheriting common
functionality from BaseClientMixin.
"""

import logging
from typing import Dict, Any

from .base_client_mixin import BaseClientMixin


class OpenAIMixin(BaseClientMixin):
    """OpenAI-specific functionality."""
    
    provider_name = "OpenAI"
    
    def _create_client(self, api_key: str):
        """Create OpenAI client."""
        try:
            from openai import OpenAI
            return OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI not available. Install with: pip install openai")
    
    def _create_completion_request(self, messages: list, **kwargs) -> Any:
        """Create OpenAI completion request."""
        return self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
            **kwargs
        ) 