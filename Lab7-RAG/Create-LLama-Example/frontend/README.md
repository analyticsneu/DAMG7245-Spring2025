# RAG Chat Application Frontend

This is a Streamlit frontend for the RAG (Retrieval-Augmented Generation) chat application backend. It provides a user-friendly interface for interacting with the RAG backend.

## Features

- Interactive chat interface
- Document upload functionality
- Visualization of tool calls made by the assistant
- Display of sources used for retrieval
- Suggested follow-up questions
- Streaming responses for real-time feedback

## Project Structure

```
frontend/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── run.py                 # Runner script
├── README.md              # This file
├── components/            # UI components
│   ├── chat_interface.py  # Chat interface component
│   ├── chat_message.py    # Message rendering
│   └── sidebar.py         # Sidebar component
└── utils/                 # Utility functions
    ├── api.py             # API communication
    └── session.py         # Session state management
```

## Setup

1. Install required dependencies:

```bash
pip install streamlit requests python-dotenv
```

2. Make sure your backend server is running.

3. Run the application:

```bash
python run.py
```

Or directly with Streamlit:

```bash
cd frontend
streamlit run app.py
```

## Configuration

The application can be configured by editing the `config.py` file or by setting environment variables.

### Environment Variables

- `BACKEND_URL`: URL of the backend server (default: http://localhost:8000)

## Integration with the Backend

This frontend integrates with the RAG backend and uses the following endpoints:

- `GET /api/chat/config`: Get chat configuration
- `POST /api/chat/upload`: Upload files
- `POST /api/chat`: Send messages (streaming)
- `POST /api/chat/request`: Send messages (non-streaming)

## Customization

The application can be customized by modifying the following files:

- `config.py`: Change configuration settings
- `components/sidebar.py`: Modify the sidebar layout
- `components/chat_interface.py`: Change the chat interface
- `components/chat_message.py`: Customize message rendering
