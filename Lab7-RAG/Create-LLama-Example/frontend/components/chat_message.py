"""
Chat message component for the Streamlit application.
"""
import streamlit as st
import json
from typing import Dict, List, Optional

def render_starter_questions():
    """
    Render starter questions if chat history is empty.
    """
    if st.session_state.chat_config.get("starterQuestions") and not st.session_state.messages:
        st.markdown("### Get started by asking:")
        
        cols = st.columns(min(3, len(st.session_state.chat_config["starterQuestions"])))
        
        for i, (col, question) in enumerate(zip(cols, st.session_state.chat_config["starterQuestions"])):
            with col:
                if st.button(question, key=f"starter_{i}"):
                    from frontend.components.chat_interface import send_message
                    send_message(question)

def render_tools(tools: List[Dict]):
    """
    Render tool calls in an expandable accordion.
    
    Args:
        tools: List of tool information
    """
    if not tools:
        return
    
    # Changed to expanded=True so tools are visible by default
    with st.expander("🔧 Tool Calls", expanded=True):
        for i, tool in enumerate(tools):
            if "title" in tool:
                st.subheader(tool["title"])
            
            if "toolCall" in tool and "toolOutput" in tool:
                tool_name = tool.get("toolCall", {}).get("name", f"Tool {i+1}")
                tool_input = tool.get("toolCall", {}).get("input", {})
                tool_output = tool.get("toolOutput", {}).get("output", "")
                is_error = tool.get("toolOutput", {}).get("isError", False)
                
                # Give tool accordions more prominence
                with st.container():
                    st.markdown(f"**{tool_name}**")
                    
                    tool_container = st.container()
                    with tool_container:
                        st.markdown("**Input:**")
                        
                        if isinstance(tool_input, dict) and tool_input:
                            st.json(tool_input)
                        else:
                            st.code(str(tool_input), language="text")
                        
                        st.markdown("**Output:**")
                        
                        if is_error:
                            st.error(str(tool_output))
                        elif isinstance(tool_output, dict):
                            st.json(tool_output)
                        else:
                            st.markdown(str(tool_output))
                # Add a divider between tools
                st.divider()
            else:
                # Fallback for other tool formats
                st.code(json.dumps(tool, indent=2), language="json")

def render_sources(sources: List[Dict]):
    """
    Render sources in an expandable accordion.
    
    Args:
        sources: List of source information
    """
    if not sources:
        return
    
    with st.expander("📚 Sources", expanded=False):
        for i, source in enumerate(sources):
            file_name = source.get("metadata", {}).get("file_name", f"Source {i+1}")
            score = source.get("score", "N/A")
            
            with st.expander(
                f"{file_name} (Score: {score:.2f})" if isinstance(score, float) else f"{file_name} (Score: {score})",
                expanded=False
            ):
                st.markdown(source.get("text", ""))
                
                if source.get("url"):
                    st.markdown(f"[View document]({source['url']})")

def render_suggested_questions(questions: List[str], on_question_click):
    """
    Render suggested follow-up questions.
    
    Args:
        questions: List of question strings
        on_question_click: Callback function when a question is clicked
    """
    if not questions:
        return
    
    st.markdown("**Suggested questions:**")
    
    # Calculate number of columns (max 3)
    num_columns = min(3, len(questions))
    cols = st.columns(num_columns)
    
    for i, (col, question) in enumerate(zip(cols, questions)):
        with col:
            if st.button(question, key=f"q_{i}"):
                on_question_click(question)

def render_chat_message(message: Dict, on_question_click=None):
    """
    Render a single chat message with tools, sources, and suggested questions.
    
    Args:
        message: Message object including content and optional tools, sources, etc.
        on_question_click: Optional callback function when a suggested question is clicked
    """
    # Don't use this function directly anymore - it's causing the duplicate issues
    # Instead, we'll handle rendering in render_chat_interface
    pass
