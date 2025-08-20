"""
HuggingFace client implementation using OpenAI-compatible API.
"""

import json
import logging
import asyncio
import base64
import os
from typing import Dict, List, Any, Optional

# Import OpenAI for HuggingFace API compatibility
try:
    from openai import OpenAI
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False
    logging.warning("HuggingFace not available. Install with: pip install openai")

from ..llm_client_base import BaseLLMClient
from ..client_utils import create_content_parts_with_embedded_names


class HuggingFaceClient(BaseLLMClient):
    """HuggingFace client using OpenAI-compatible API for vision models."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if not HUGGINGFACE_AVAILABLE:
            raise ImportError("HuggingFace not available")
        
        # Initialize OpenAI client with HuggingFace base URL
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=config["api_key"]
        )
        self.model_id = config["model"]
    
    def call_llm(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str, 
                 strategy_type: Optional[str] = None) -> Dict[str, Any]:
        """Call HuggingFace with user prompt, optional system prompt, and files."""
        
        # HuggingFace only supports image_first strategy for vision models
        if strategy_type in ["direct_file", "text_first"]:
            error_msg = f"HuggingFace does not support {strategy_type} strategy. Use image_first strategy instead."
            logging.error(f"❌ {error_msg}")
            return {"error": error_msg}
        
        # Check if this is image first strategy with HuggingFace
        if strategy_type == "image_first" and files:
            return self._call_llm_image_first(files=files, system_prompt=system_prompt, user_prompt=user_prompt)
        
        # Standard HuggingFace processing for other strategies
        return self._call_llm_standard(files=files, system_prompt=system_prompt, user_prompt=user_prompt)
    
    def _call_llm_image_first(self, *, files: List[str], system_prompt: Optional[str] = None, user_prompt: str) -> Dict[str, Any]:
        """
        Process images with HuggingFace vision models using image_first strategy.
        """
        try:
            logging.info(f"🔄 Using HuggingFace image first strategy with {len(files)} files")
            
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add user message with image handling and filename embedding
            content_parts = create_content_parts_with_embedded_names(
                files=files,
                original_filenames=[os.path.basename(f) for f in files],
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                is_image_mode=True
            )
            
            # Convert content parts to HuggingFace format
            user_message = {"role": "user", "content": []}
            
            for part in content_parts:
                if part.get("text"):
                    user_message["content"].append({
                        "type": "text",
                        "text": part["text"]
                    })
                elif part.get("inline_data"):
                    # Convert inline_data to image_url format for HuggingFace
                    user_message["content"].append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{part['inline_data']['mime_type']};base64,{part['inline_data']['data']}"
                        }
                    })
            

            
            messages.append(user_message)
            
            # Call HuggingFace API
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Debug: Log the raw response using centralized logging utility
            from llm_client.llm_response_logging import log_llm_response
            log_llm_response("HuggingFace", completion)
            
            # Extract response
            response_text = completion.choices[0].message.content
            
            # Try to parse as JSON
            try:
                result = json.loads(response_text)
                logging.info(f"✅ HuggingFace response parsed successfully")
                return result
            except json.JSONDecodeError:
                # Truncate content to prevent large log files
                truncated_response = response_text[:500] + "..." if len(response_text) > 500 else response_text
                logging.warning(f"⚠️ HuggingFace response is not valid JSON (truncated): {truncated_response}")
                return {"error": f"Invalid JSON response: {response_text}"}
                
        except Exception as e:
            error_msg = f"HuggingFace API error: {str(e)}"
            logging.error(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def _call_llm_standard(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str) -> Dict[str, Any]:
        """
        Standard HuggingFace processing without files.
        """
        try:
            logging.info(f"🔄 Using HuggingFace standard processing")
            
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add user message
            messages.append({"role": "user", "content": user_prompt})
            
            # Call HuggingFace API
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Debug: Log the raw response using centralized logging utility
            from llm_client.llm_response_logging import log_llm_response
            log_llm_response("HuggingFace", completion)
            
            # Extract response
            response_text = completion.choices[0].message.content
            
            # Try to parse as JSON
            try:
                result = json.loads(response_text)
                logging.info(f"✅ HuggingFace response parsed successfully")
                return result
            except json.JSONDecodeError:
                # Truncate content to prevent large log files
                truncated_response = response_text[:500] + "..." if len(response_text) > 500 else response_text
                logging.warning(f"⚠️ HuggingFace response is not valid JSON (truncated): {truncated_response}")
                return {"error": f"Invalid JSON response: {response_text}"}
                
        except Exception as e:
            error_msg = f"HuggingFace API error: {str(e)}"
            logging.error(f"❌ {error_msg}")
            return {"error": error_msg}
    
    async def call_llm_async(self, *, files: Optional[List[str]] = None, system_prompt: Optional[str] = None, user_prompt: str,
                           strategy_type: Optional[str] = None) -> Dict[str, Any]:
        """Call HuggingFace asynchronously."""
        # For now, use synchronous version in async context
        # TODO: Implement proper async version if needed
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.call_llm, 
                                         files, system_prompt, user_prompt, strategy_type) 