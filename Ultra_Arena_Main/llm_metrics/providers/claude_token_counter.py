"""
Claude token counter implementation.
"""

import logging
import os
from typing import Dict, Any, List

from ..llm_token_counter_base import BaseTokenCounter


class ClaudeTokenCounter(BaseTokenCounter):
    """Claude token counter using Anthropic's tokenizer."""
    
    def __init__(self, client):
        """Initialize with Claude client."""
        super().__init__(client)
        self.model_name = "claude-sonnet-4-20250514"
        
        # Check if the client has the count_tokens method
        if hasattr(client, 'count_tokens'):
            self._api_available = True
            logging.info("Claude API token counting available")
        else:
            self._api_available = False
            logging.warning("Claude API token counting not available, using fallback estimation")
    
    def count_text_tokens(self, text: str) -> int:
        """Count tokens in text using Claude's API."""
        # For Claude, we avoid API-based token counting to prevent post-LLM token counting errors
        # We use fallback estimation since actual token usage comes from LLM response
        return self._fallback_token_count(text)
    
    def get_model_name(self) -> str:
        """Get the model name used for token counting."""
        return self.model_name
    
    def count_prompt_tokens(self, prompt: str, files: List[str] = None, system_prompt: str = None) -> int:
        """Count tokens for a complete prompt including files."""
        # For Claude, we avoid API-based token counting to prevent post-LLM token counting errors
        # We use fallback estimation since actual token usage comes from LLM response
        return self._fallback_prompt_token_count(prompt, files, system_prompt)
    
    def count_file_content_tokens(self, file_path: str) -> int:
        """Count tokens in file content - optimized for Claude API."""
        if self._api_available:
            # For Claude with API available, we avoid individual file token counting
            # to reduce API calls. We'll use the batch approach instead.
            # This is a rough estimation based on file size
            return self._fallback_file_token_estimation(file_path)
        else:
            # Fallback to base class method
            return super().count_file_content_tokens(file_path)
    
    def _fallback_prompt_token_count(self, prompt: str, files: List[str] = None, system_prompt: str = None) -> int:
        """Fallback token counting for prompts with files."""
        total_tokens = 0
        
        # Count system prompt tokens
        if system_prompt:
            total_tokens += self._fallback_token_count(system_prompt)
        
        # Count user prompt tokens
        total_tokens += self._fallback_token_count(prompt)
        
        # Estimate file tokens (rough estimation)
        if files:
            for file_path in files:
                # Estimate based on file size and type
                try:
                    file_size = os.path.getsize(file_path)
                    # Rough estimate: 1 token per 4 characters for text files
                    estimated_tokens = file_size // 4
                    total_tokens += estimated_tokens
                except:
                    # If we can't get file size, estimate based on filename
                    total_tokens += 100  # Conservative estimate
        
        return total_tokens
    
    def count_multi_file_request_tokens(self, prompt: str, file_paths: List[str]) -> Dict[str, int]:
        """Count tokens for a multi-file request including prompt and all file contents."""
        # For Claude, we avoid API-based token counting to prevent post-LLM token counting errors
        # We use fallback estimation since actual token usage comes from LLM response
        try:
            # Count prompt tokens
            prompt_tokens = self.count_prompt_tokens(prompt, file_paths)
            
            # Count file content tokens
            file_tokens = {}
            total_file_tokens = 0
            
            for file_path in file_paths:
                file_token_count = self.count_file_content_tokens(file_path)
                file_tokens[file_path] = file_token_count
                total_file_tokens += file_token_count
            
            # Estimate request structure overhead (JSON structure, file_data wrappers, etc.)
            request_overhead = len(file_paths) * 50  # Rough estimate per file
            
            total_tokens = prompt_tokens + total_file_tokens + request_overhead
            
            return {
                'prompt_tokens': prompt_tokens,
                'file_tokens': file_tokens,
                'request_overhead': request_overhead,
                'total_input_tokens': total_tokens,
                'estimated_response_tokens': int(total_file_tokens * 0.8)  # LLM typically generates substantial response
            }
            
        except Exception as e:
            logging.warning(f"Failed to count multi-file request tokens: {e}")
            return self._fallback_multi_file_estimation(prompt, file_paths)
    
    def _fallback_multi_file_estimation(self, prompt: str, file_paths: List[str]) -> Dict[str, int]:
        """Fallback estimation for multi-file requests."""
        prompt_tokens = len(prompt.split()) * 1.3
        file_tokens = {fp: self._fallback_file_token_estimation(fp) for fp in file_paths}
        total_file_tokens = sum(file_tokens.values())
        
        return {
            'prompt_tokens': int(prompt_tokens),
            'file_tokens': file_tokens,
            'request_overhead': len(file_paths) * 50,
            'total_input_tokens': int(prompt_tokens) + total_file_tokens + len(file_paths) * 50,
            'estimated_response_tokens': int(total_file_tokens * 0.8)
        }
    
    def _fallback_file_token_estimation(self, file_path: str) -> int:
        """Fallback token estimation for files."""
        try:
            file_size = os.path.getsize(file_path)
            return file_size // 4  # Rough estimate: 1 token per 4 characters
        except:
            return 1000  # Default fallback
    
    def _fallback_token_count(self, text: str) -> int:
        """Fallback token counting when Claude tokenizer is not available."""
        # Improved estimation for Claude models
        # Based on typical tokenization patterns for Claude
        # Words are roughly 1.3 tokens each, with some overhead for special characters
        
        # Count words and apply a more accurate multiplier
        words = text.split()
        word_count = len(words)
        
        # Estimate tokens: words * 1.3 + overhead for special characters and formatting
        estimated_tokens = int(word_count * 1.3) + len(text) // 100  # Add overhead for special chars
        
        return max(estimated_tokens, 1)  # Ensure at least 1 token 