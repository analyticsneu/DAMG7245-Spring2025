"""Main Streamlit application file."""
import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.config import APP_TITLE, APP_ICON, APP_DESCRIPTION
from frontend.utils.session import initialize_session_state, is_processing
from frontend.utils.api import get_chat_config
from frontend.components.sidebar import render_sidebar
from frontend.components.chat_interface import send_message
from frontend.components.chat_message import render_starter_questions, render_tools, render_sources


def display_chat_history():
    """
    Display the chat history in a simple, consistent way.
    This follows Streamlit's recommended pattern for chat applications.
    """
    # Get the chat history from session state
    messages = st.session_state.messages
    
    # Display each message in order
    for i, message in enumerate(messages):
        # User message
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        
        # Assistant message
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                # First display tools if present
                if "tools" in message and message["tools"]:
                    render_tools(message["tools"])
                
                # Then display the main content
                st.markdown(message["content"])
                
                # Then display sources if present
                if "sources" in message and message["sources"]:
                    render_sources(message["sources"])
            
            # Display suggested questions outside of the chat message container
            if "suggested_questions" in message and message["suggested_questions"]:
                questions = message["suggested_questions"]
                st.markdown("**Suggested questions:**")
                
                # Display in columns
                cols = st.columns(min(3, len(questions)))
                for j, (col, question) in enumerate(zip(cols, questions)):
                    with col:
                        # Use a unique key for each button
                        key = f"sq_{i}_{j}_{hash(question) % 10000}"
                        if st.button(question, key=key, use_container_width=True):
                            st.session_state.next_question = question
                            st.rerun()

def main():
    """
    Main application function.
    """
    # Configure page
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Fetch chat configuration if not already available
    if not st.session_state.chat_config:
        st.session_state.chat_config = get_chat_config()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown(APP_DESCRIPTION)
    
    # Process pending questions first (without calling rerun)
    if hasattr(st.session_state, 'next_question') and st.session_state.next_question:
        question = st.session_state.next_question
        st.session_state.next_question = None
        send_message(question)
    
    # Render starter questions if no messages
    if not st.session_state.messages:
        render_starter_questions()
    
    # Display chat history
    display_chat_history()
    
    # Chat input must be the LAST UI element to ensure it stays at the bottom
    # This is crucial for Streamlit's layout flow
    if prompt := st.chat_input("Type your message here...", disabled=st.session_state.is_processing):
        send_message(prompt)
    # Add custom CSS for better styling
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu, footer {visibility: hidden;}
    
    /* Improve chat message styling */
    .stChatMessage {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Add padding to the bottom to ensure content isn't hidden */
    body {
        padding-bottom: 5rem;
    }
    
    /* Style user messages to be on the right */
    .stChatMessage[data-testid="user-message"] {
        background-color: #0084ff !important;
        border-bottom-right-radius: 0 !important;
        margin-left: 20% !important;
    }
    
    /* Style assistant messages to be on the left */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #383838 !important;
        border-bottom-left-radius: 0 !important;
        margin-right: 20% !important;
    }
    
    /* Improve button styling for suggested questions */
    .stButton button {
        border-radius: 20px;
        padding: 2px 15px;
        font-size: 0.9em;
        border: 1px solid rgba(128, 128, 128, 0.4);
        background-color: rgba(128, 128, 128, 0.1);
    }
    
    /* Add some padding to expanders */
    .streamlit-expanderHeader {
        font-size: 1em;
        font-weight: 600;
    }
    
    /* Improve tool styling */
    .streamlit-expanderContent {
        padding: 0.5rem;
        background-color: rgba(128, 128, 128, 0.05);
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
