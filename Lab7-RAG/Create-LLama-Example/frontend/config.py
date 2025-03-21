"""
Configuration file for the Streamlit frontend application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# UI Configuration
APP_TITLE = "RAG Chat Application"
APP_ICON = "📚"
APP_DESCRIPTION = "Chat with your documents using Retrieval-Augmented Generation"

# File Upload Configuration
ALLOWED_FILE_TYPES = ["pdf", "txt", "docx", "csv", "json", "md", "html"]
MAX_FILE_SIZE = 10  # in MB

# Default system prompt - can be shown to users
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful assistant who helps users with their questions, using the knowledge base and tools provided to you.",
)
