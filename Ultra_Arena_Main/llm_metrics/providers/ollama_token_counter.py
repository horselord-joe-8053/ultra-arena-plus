"""
Token counter for Ollama LLM provider.
This is a simple implementation that returns 0 for all token counts.
"""

import logging
from typing import List, Dict, Any
from ..llm_token_counter_base import BaseTokenCounter

logger = logging.getLogger(__name__)


class LocalOllamaTokenCounter(BaseTokenCounter):
    """Token counter for Ollama LLM provider that returns 0 for all counts."""
    
    def __init__(self, llm_client=None):
        """Initialize the Ollama token counter."""
        super().__init__(llm_client)
        logger.info("🔧 Initialized LocalOllamaTokenCounter")
    
    def count_text_tokens(self, text: str) -> int:
        """Count tokens in text. Returns 0 for Ollama."""
        logger.debug(f"🔍 Counting tokens for text (length: {len(text)}) - returning 0")
        return 0
    
    def count_prompt_tokens(self, prompt: str) -> int:
        """Count tokens in prompt. Returns 0 for Ollama."""
        logger.debug(f"🔍 Counting tokens for prompt (length: {len(prompt)}) - returning 0")
        return 0
    
    def count_multi_file_request_tokens(self, files: List[str], user_prompt: str = "") -> int:
        """Count tokens in multi-file request. Returns 0 for Ollama."""
        logger.debug(f"🔍 Counting tokens for multi-file request ({len(files)} files) - returning 0")
        return 0
    
    def _fallback_token_count(self, text: str) -> int:
        """Fallback token counting method. Returns 0 for Ollama."""
        logger.debug(f"🔍 Fallback token count for text (length: {len(text)}) - returning 0")
        return 0
    
    def get_model_name(self) -> str:
        """Get the model name used for token counting."""
        return "ollama-local" 