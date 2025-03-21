"""
Sidebar component for the Streamlit application.
"""
import streamlit as st
from typing import List, Dict

from frontend.config import ALLOWED_FILE_TYPES, MAX_FILE_SIZE
from frontend.utils.api import upload_file
from frontend.utils.session import add_file, clear_files

def render_sidebar():
    """
    Render the sidebar with file upload functionality.
    """
    with st.sidebar:
        st.header("Document Upload")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Select a file",
            type=ALLOWED_FILE_TYPES,
            accept_multiple_files=False,
            help=f"Upload files to chat with. Supported types: {', '.join(ALLOWED_FILE_TYPES)}. Max size: {MAX_FILE_SIZE}MB."
        )
        
        # Add file button
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > MAX_FILE_SIZE:
                st.error(f"File size exceeds maximum limit of {MAX_FILE_SIZE}MB")
            elif st.button("Add File", type="primary"):
                with st.spinner("Uploading file..."):
                    try:
                        file_info = upload_file(uploaded_file)
                        add_file(file_info)
                        st.success(f"File {uploaded_file.name} added successfully!")
                    except Exception as e:
                        st.error(f"Error uploading file: {str(e)}")
        
        # Display uploaded files
        if st.session_state.files:
            st.subheader("Uploaded Files")
            
            for i, file in enumerate(st.session_state.files):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text(file["name"])
                with col2:
                    if st.button("❌", key=f"remove_{i}", help="Remove this file"):
                        st.session_state.files.pop(i)
                        st.rerun()
            
            # Clear all files button
            if len(st.session_state.files) > 1 and st.button("Clear All Files"):
                clear_files()
                st.rerun()
        
        # Add additional sidebar elements
        st.divider()
        st.header("About")
        st.markdown("""
        This application allows you to chat with your documents using Retrieval-Augmented Generation.
        
        **Features:**
        - Upload documents to chat with
        - Ask questions about your documents
        - View sources and references
        - See tool calls used by the assistant
        """)
        
        # Add GitHub repository link
        st.markdown("[View on GitHub](https://github.com/your-repository-link)")
