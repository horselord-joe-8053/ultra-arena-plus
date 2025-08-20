"""
TogetherAI token counter implementation.

This module reuses the OpenAI token counter since TogetherAI models
use similar tokenization schemes.
"""

import logging
from ..llm_token_counter_base import BaseTokenCounter


class TogetherAITokenCounter(BaseTokenCounter):
    """Token counter for TogetherAI models using tiktoken."""
    
    def __init__(self, client, model_name: str = "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo"):
        super().__init__(client)
        self.model_name = model_name
        try:
            import tiktoken
            # Use cl100k_base encoding for TogetherAI models (similar to GPT models)
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except ImportError:
            logging.warning("tiktoken not available, using fallback estimation")
            self.encoding = None
        except Exception as e:
            logging.warning(f"Failed to initialize tiktoken for {model_name}: {e}")
            self.encoding = None
    
    def count_text_tokens(self, text: str) -> int:
        """Count tokens in plain text using tiktoken."""
        try:
            if self.encoding:
                return len(self.encoding.encode(text))
            else:
                # Fallback: rough estimation
                return len(text.split()) * 1.3
        except Exception as e:
            logging.warning(f"Failed to count tokens for text: {e}")
            return len(text.split()) * 1.3
    
    def get_model_name(self) -> str:
        return self.model_name 