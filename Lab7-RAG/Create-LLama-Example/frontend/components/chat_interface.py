"""
Chat interface component for the Streamlit application.
"""
import streamlit as st
import requests
import json
from typing import List, Dict, Any, Callable

from frontend.config import BACKEND_URL
from frontend.utils.api import process_streaming_line
from frontend.utils.session import add_message, get_message_history, start_processing, end_processing
from frontend.components.chat_message import render_chat_message

def render_chat_history(on_question_click: Callable[[str], None]):
    """
    Render the chat history.
    
    Args:
        on_question_click: Callback function when a suggested question is clicked
    """
    # Display chat history
    for message in get_message_history():
        render_chat_message(message, on_question_click)

def render_streaming_message(response) -> Dict:
    """
    Render streaming message from the backend.
    
    Args:
        response: Streaming response object
        
    Returns:
        Dict: Complete message after streaming
    """
    # Variables to collect data from streaming response
    tools = []
    sources = []
    suggested_questions = []
    content = ""
    
    # Create a placeholder for streaming content
    message_placeholder = st.empty()
    
    # Process the streaming response line by line
    for line in response.iter_lines():
        if not line:
            continue
            
        line = line.decode('utf-8')
        processed = process_streaming_line(line)
        
        if processed["type"] == "text":
            content += processed["data"]
            # Update display with current content
            message_placeholder.markdown(content)
            
        elif processed["type"] == "data" and processed["data"]:
            data = processed["data"]
            data_type = data.get("type")
            
            if data_type == "events":
                tools.append(data.get("data", {}))
                
            elif data_type == "sources":
                sources = data.get("data", {}).get("nodes", [])
                
            elif data_type == "suggested_questions":
                suggested_questions = data.get("data", [])
                
            elif data_type == "tools":
                tools.append(data.get("data", {}))
                
        elif processed["type"] == "error":
            content = f"Error: {processed['data']}"
            message_placeholder.markdown(content)
    
    # *** IMPORTANT CHANGE: Don't clear the placeholder to keep content visible ***
    # Instead, leave the content visible until the next rerun
    
    # Return the complete message
    return {
        "role": "assistant",
        "content": content,
        "sources": sources,
        "tools": tools,
        "suggested_questions": suggested_questions
    }

def send_message(message: str):
    """
    Send a message to the backend and process the response.
    This function doesn't render UI elements - that happens in display_chat_history.
    
    Args:
        message: User message
    """
    # Mark processing as started
    start_processing()
    
    try:
        # Add user message to chat history
        add_message("user", message)
        
        # Prepare the payload
        payload = {
            "messages": [
                {"role": msg["role"], "content": msg["content"]}
                for msg in get_message_history()
            ]
        }
        
        # Add file annotations if any
        if st.session_state.files:
            payload["messages"][-1]["annotations"] = [{
                "type": "document_file",
                "data": {"files": st.session_state.files}
            }]
            
            # Clear files after sending
            st.session_state.files = []
        
        # Show a status message during processing
        with st.chat_message("assistant"):
            status = st.empty()
            status.info("Processing your request...")
            
            # Send the request and process the streaming response
            with requests.post(f"{BACKEND_URL}/api/chat", json=payload, stream=True) as response:
                response.raise_for_status()
                assistant_message = render_streaming_message(response)
        
        # Add the response to chat history
        add_message(
            "assistant",
            assistant_message["content"],
            sources=assistant_message["sources"],
            tools=assistant_message["tools"],
            suggested_questions=assistant_message["suggested_questions"]
        )
        
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        # Add error message to chat history
        add_message("assistant", f"Error: {str(e)}")
    
    finally:
        # Mark processing as ended
        end_processing()




