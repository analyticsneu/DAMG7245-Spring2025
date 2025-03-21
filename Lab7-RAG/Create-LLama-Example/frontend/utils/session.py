"""
Session state manager for the Streamlit application.
"""
import streamlit as st
from typing import List, Dict, Any, Optional

def initialize_session_state():
    """
    Initialize session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "files" not in st.session_state:
        st.session_state.files = []
    
    if "chat_config" not in st.session_state:
        st.session_state.chat_config = {}
    
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False
        
    if "next_question" not in st.session_state:
        st.session_state.next_question = None

def add_message(role: str, content: str, **kwargs):
    """
    Add a message to the session state.
    
    Args:
        role: Role of the message sender ('user' or 'assistant')
        content: Content of the message
        kwargs: Additional message attributes
    """
    message = {"role": role, "content": content, **kwargs}
    st.session_state.messages.append(message)

def get_last_user_message() -> Optional[Dict]:
    """
    Get the last user message from the session state.
    
    Returns:
        Dict or None: The last user message or None if no user messages exist
    """
    for message in reversed(st.session_state.messages):
        if message["role"] == "user":
            return message
    return None

def add_file(file_info: Dict):
    """
    Add a file to the session state.
    
    Args:
        file_info: File information
    """
    st.session_state.files.append(file_info)

def clear_files():
    """
    Clear all files from the session state.
    """
    st.session_state.files = []

def get_message_history() -> List[Dict]:
    """
    Get the message history from the session state.
    
    Returns:
        List[Dict]: List of messages
    """
    return st.session_state.messages

def start_processing():
    """
    Mark the start of message processing.
    """
    st.session_state.is_processing = True

def end_processing():
    """
    Mark the end of message processing.
    """
    st.session_state.is_processing = False

def is_processing() -> bool:
    """
    Check if a message is being processed.
    
    Returns:
        bool: True if a message is being processed, False otherwise
    """
    return st.session_state.is_processing

def set_next_question(question: str):
    """
    Set the next question to be processed.
    
    Args:
        question: The question to process
    """
    st.session_state.next_question = question
    # No longer trigger rerun immediately - we'll let the main app handle it in a controlled way

def get_next_question() -> Optional[str]:
    """
    Get the next question to be processed.
    
    Returns:
        str or None: The next question or None if no question is set
    """
    if hasattr(st.session_state, 'next_question'):
        return st.session_state.next_question
    return None

def clear_next_question():
    """
    Clear the next question.
    """
    st.session_state.next_question = None
