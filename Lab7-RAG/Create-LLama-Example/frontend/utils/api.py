"""
API utilities for communicating with the backend.
"""
import requests
import json
import base64
from typing import Dict, List, Any
import streamlit as st

from frontend.config import BACKEND_URL

def encode_file(file) -> str:
    """
    Encode file content to base64.
    
    Args:
        file: The uploaded file object
        
    Returns:
        str: Base64 encoded file content with MIME type
    """
    content = file.read()
    file.seek(0)  # Reset file pointer to beginning
    encoded = base64.b64encode(content).decode()
    mime_type = file.type or "application/octet-stream"
    return f"data:{mime_type};base64,{encoded}"

def upload_file(file) -> Dict:
    """
    Upload file to backend and return file info.
    
    Args:
        file: The uploaded file object
        
    Returns:
        Dict: File information returned by the backend
    """
    file_data = {
        "base64": encode_file(file),
        "name": file.name
    }
    
    response = requests.post(f"{BACKEND_URL}/api/chat/upload", json=file_data)
    response.raise_for_status()
    return response.json()

def get_chat_config() -> Dict:
    """
    Get chat configuration from the backend.
    
    Returns:
        Dict: Chat configuration
    """
    try:
        response = requests.get(f"{BACKEND_URL}/api/chat/config")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to get chat configuration: {str(e)}")
        return {"starterQuestions": []}

def send_chat_message(messages: List[Dict], files: List[Dict] = None) -> Dict:
    """
    Send a chat message to the backend. Non-streaming version for testing.
    
    Args:
        messages: List of message objects
        files: List of file information objects
        
    Returns:
        Dict: Response from the backend
    """
    # Create a copy of the last message to avoid modifying the original
    last_message = messages[-1].copy()
    
    # Add file annotations if any
    if files:
        last_message["annotations"] = [{
            "type": "document_file",
            "data": {"files": files}
        }]
    
    # Replace the last message with the modified one
    payload = {
        "messages": messages[:-1] + [last_message]
    }
    
    response = requests.post(f"{BACKEND_URL}/api/chat/request", json=payload)
    response.raise_for_status()
    return response.json()

def process_streaming_line(line: str) -> Dict:
    """
    Process a single line from the streaming response.
    
    Args:
        line: Line from the streaming response
        
    Returns:
        Dict: Processed data from the line
    """
    if not line:
        return {"type": None, "data": None}
    
    # Handle text chunks (content)
    if line.startswith("0:"):
        try:
            text_chunk = json.loads(line[2:])
            return {"type": "text", "data": text_chunk}
        except json.JSONDecodeError:
            return {"type": "error", "data": "Failed to parse text chunk"}
    
    # Handle data chunks (tools, sources, etc.)
    elif line.startswith("8:"):
        try:
            data = json.loads(line[2:])
            if isinstance(data, list) and len(data) > 0:
                return {"type": "data", "data": data[0]}
            return {"type": "data", "data": None}
        except json.JSONDecodeError:
            return {"type": "error", "data": "Failed to parse data chunk"}
    
    # Handle error chunks
    elif line.startswith("3:"):
        try:
            error = json.loads(line[2:])
            return {"type": "error", "data": error}
        except json.JSONDecodeError:
            return {"type": "error", "data": "Failed to parse error chunk"}
    
    return {"type": None, "data": None}
