"""
TogetherAI client implementation.

This module uses the TogetherAI mixin to provide TogetherAI-specific functionality
while inheriting common functionality from BaseClientMixin.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional

from ..llm_client_base import BaseLLMClient
from .togetherai_mixin import TogetherAIMixin


class TogetherAIClient(TogetherAIMixin, BaseLLMClient):
    """TogetherAI client for direct file processing."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = self._create_client(config["api_key"])
        self.model_id = config["model"]
    
    def call_llm(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str, 
                 strategy_type: Optional[str] = None) -> Dict[str, Any]:
        """Call TogetherAI with user prompt, optional system prompt, and files."""
        
        # Validate strategy using mixin
        validation_error = self._validate_strategy(strategy_type)
        if validation_error:
            return validation_error
        
        # Check if this is image first strategy with TogetherAI - apply special treatment
        if strategy_type == "image_first" and files:
            return self._call_llm_image_first_special(files=files, system_prompt=system_prompt, user_prompt=user_prompt)
        
        # Standard TogetherAI processing for other strategies
        return self._call_llm_standard(files=files, system_prompt=system_prompt, user_prompt=user_prompt)
    
    def _call_llm_image_first_special(self, *, files: List[str], system_prompt: Optional[str] = None, user_prompt: str) -> Dict[str, Any]:
        """
        Special treatment for TogetherAI with image first strategy.
        
        This method implements the specific logic needed for TogetherAI when processing images
        in the image first strategy, which may differ from standard file processing.
        """
        try:
            logging.info(f"🔄 Using TogetherAI special treatment for image first strategy with {len(files)} files")
            
            # Build message content using mixin
            user_content = self._build_image_message_content(user_prompt, files)
            
            # Create messages using mixin
            messages = self._create_messages(system_prompt, user_content)
            
            # Create completion request using mixin
            response = self._create_completion_request(messages)
            
            # Log response using mixin
            self._log_llm_response(response)
            
            # Parse response using mixin
            result = self._parse_response(response.choices[0].message.content)
            
            # Add token usage using mixin
            self._add_token_usage_to_result(result, response)
            
            return result
            
        except Exception as e:
            logging.error(f"TogetherAI image first special treatment error: {e}")
            return {"error": str(e)}
    

    
    def _call_llm_standard(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str) -> Dict[str, Any]:
        """Standard TogetherAI processing for non-image-first strategies."""
        try:
            # Build message content using mixin
            user_content = self._build_standard_message_content(user_prompt, files)
            
            # Create messages using mixin
            messages = self._create_messages(system_prompt, user_content)
            
            # Create completion request using mixin
            response = self._create_completion_request(messages)
            
            # Log response using mixin
            self._log_llm_response(response)
            
            # Parse response using mixin
            result = self._parse_response(response.choices[0].message.content)
            
            # Add token usage using mixin
            self._add_token_usage_to_result(result, response)
            
            return result
            
        except Exception as e:
            logging.error(f"TogetherAI API error: {e}")
            return {"error": str(e)}
    
    async def call_llm_async(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str,
                           strategy_type: Optional[str] = None) -> Dict[str, Any]:
        """Call TogetherAI asynchronously."""
        # Run in thread pool since TogetherAI doesn't have async API in this context
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.call_llm, files=files, system_prompt=system_prompt, user_prompt=user_prompt, strategy_type=strategy_type) 