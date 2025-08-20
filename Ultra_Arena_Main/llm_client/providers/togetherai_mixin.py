"""
TogetherAI-specific mixin for OpenAI-style clients.

This mixin provides TogetherAI-specific functionality while inheriting common
functionality from BaseClientMixin.
"""

import logging
from typing import Dict, Any

from .base_client_mixin import BaseClientMixin


class TogetherAIMixin(BaseClientMixin):
    """TogetherAI-specific functionality."""
    
    provider_name = "TogetherAI"
    
    def _create_client(self, api_key: str):
        """Create TogetherAI client."""
        try:
            from together import Together
            return Together(api_key=api_key)
        except ImportError:
            raise ImportError("TogetherAI not available. Install with: pip install together")
    
    def _create_completion_request(self, messages: list, **kwargs) -> Any:
        """Create TogetherAI completion request."""
        return self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
            **kwargs
        ) 