"""
Grok token counter implementation.

This module provides token counting functionality for Grok models.
"""

import logging
import tiktoken
from typing import Dict, Any, List

from ..llm_token_counter_base import BaseTokenCounter


class GrokTokenCounter(BaseTokenCounter):
    """Token counter for Grok models."""
    
    def __init__(self, client, model_id: str):
        super().__init__(client)
        self.model_id = model_id
        # Grok uses the same tokenizer as OpenAI (cl100k_base)
        self.encoding = tiktoken.get_encoding("cl100k_base")
        logging.info(f"Initialized grok token counter with model: {model_id}")
    
    def count_text_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken."""
        return len(self.encoding.encode(text))
    
    def get_model_name(self) -> str:
        """Get the model name used for token counting."""
        return self.model_id
    
    def count_tokens_in_messages(self, messages: List[Dict[str, Any]]) -> int:
        """Count tokens in a list of messages."""
        total_tokens = 0
        for message in messages:
            if isinstance(message.get("content"), str):
                total_tokens += self.count_text_tokens(message["content"])
            elif isinstance(message.get("content"), list):
                # Handle multimodal content (text + images)
                for content_item in message["content"]:
                    if content_item.get("type") == "text":
                        total_tokens += self.count_text_tokens(content_item["text"])
                    elif content_item.get("type") == "image_url":
                        # Estimate tokens for images (rough approximation)
                        total_tokens += 85  # Base cost for image
        return total_tokens 