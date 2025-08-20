"""
Utility functions for LLM clients to handle common operations like filename embedding.
"""

def _create_filename_embedded_prompt(user_prompt, file_type="file", example_filename=None):
    """Create an enhanced prompt with filename embedding instructions.
    
    Args:
        user_prompt: The original user prompt
        file_type: Type of file being processed ("file", "image", etc.)
        example_filename: Example filename to show in the format (e.g., "document1.pdf")
    
    Returns:
        Enhanced prompt with filename extraction instructions
    """
    if example_filename is None:
        example_filename = f"document1.{'png' if file_type == 'image' else 'pdf'}"
    
    enhanced_prompt = (
        f"{user_prompt}\n\n"
        f"Analyze each uploaded {file_type} and return a JSON array. "
        "For each file, look for the filename markers (=== FILE: ... ===) and include "
        "that EXACT filename in your response. Each object MUST include a 'file_name_llm' field "
        "that matches the filename from the markers. Example format:\n"
        "[\n"
        "    {\n"
        f'        "file_name_llm": "{example_filename}",\n'
        '        "...": "...",\n'
        "    }\n"
        "]"
    )
    return enhanced_prompt

def _create_text_first_prompt(user_prompt, example_filename=None):
    """Create an enhanced prompt for text-first strategy with text content embedding instructions.
    
    Args:
        user_prompt: The original user prompt
        example_filename: Example filename to show in the format (e.g., "document1.pdf")
    
    Returns:
        Enhanced prompt with text content extraction instructions
    """
    if example_filename is None:
        example_filename = "document1.pdf"
    
    enhanced_prompt = (
        f"{user_prompt}\n\n"
        "Analyze each text block and return a JSON array. "
        "For each text block, look for the filename markers (=== FILE: ... ===) and include "
        "that EXACT filename in your response. Each object MUST include a 'file_name_llm' field "
        "that matches the filename from the markers. Example format:\n"
        "[\n"
        "    {\n"
        f'        "file_name_llm": "{example_filename}",\n'
        '        "...": "...",\n'
        "    }\n"
        "]"
    )
    return enhanced_prompt

def create_text_first_content_parts(text_contents, original_filenames, system_prompt=None, user_prompt=""):
    """Create content parts for text-first strategy with embedded text content.
    
    Args:
        text_contents: List of extracted text content from PDFs
        original_filenames: List of original PDF filenames
        system_prompt: Optional system prompt
        user_prompt: User prompt
        
    Returns:
        List of content parts with embedded text content and filename markers
    """
    parts = []
    
    # Add system prompt if provided
    if system_prompt:
        parts.append({"text": system_prompt})
    
    # Add enhanced user prompt with text content instructions
    enhanced_prompt = _create_text_first_prompt(user_prompt)
    parts.append({"text": enhanced_prompt})
    
    # Add text contents with embedded filename markers
    for text_content, original_filename in zip(text_contents, original_filenames):
        # Add start marker
        parts.append({"text": f"=== FILE: {original_filename} ==="})
        
        # Add the extracted text content
        parts.append({"text": text_content})
        
        # Add end marker
        parts.append({"text": f"=== END FILE: {original_filename} ==="})
    
    return parts

def create_content_parts_with_embedded_names(files, original_filenames, system_prompt=None, 
                                           user_prompt="", is_image_mode=False, 
                                           file_uri_getter=None, mime_type="image/png"):
    """Create content parts with embedded filenames for better LLM understanding.
    
    Args:
        files: List of uploaded file objects (for PDFs) or file paths (for images)
        original_filenames: List of original filenames
        system_prompt: Optional system prompt
        user_prompt: User prompt
        is_image_mode: If True, treat files as image file paths and use inline_data
        file_uri_getter: Function to get file URI from file object (for non-image files)
        mime_type: MIME type for image files (default: "image/png")
        
    Returns:
        List of content parts with embedded filename markers
    """
    parts = []
    
    # Add system prompt if provided
    if system_prompt:
        parts.append({"text": system_prompt})
    
    # Determine file type for prompt
    file_type = "image" if is_image_mode else "file"
    example_filename = "document1.png" if is_image_mode else "document1.pdf"
    
    # Add enhanced user prompt with filename instructions
    enhanced_prompt = _create_filename_embedded_prompt(user_prompt, file_type, example_filename)
    parts.append({"text": enhanced_prompt})
    
    # Add files with embedded filename markers
    for file_item, original_filename in zip(files, original_filenames):
        # Add start marker
        parts.append({"text": f"=== FILE: {original_filename} ==="})
        
        if is_image_mode:
            # For images: read file and convert to base64
            import base64
            with open(file_item, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            parts.append({"inline_data": {"mime_type": mime_type, "data": image_data}})
        else:
            # For PDFs: use uploaded file URI
            if file_uri_getter:
                file_uri = file_uri_getter(file_item)
            else:
                # Default assumption for Google GenAI
                file_uri = file_item.uri
            parts.append({"file_data": {"file_uri": file_uri}})
        
        # Add end marker
        parts.append({"text": f"=== END FILE: {original_filename} ==="})
    
    return parts 