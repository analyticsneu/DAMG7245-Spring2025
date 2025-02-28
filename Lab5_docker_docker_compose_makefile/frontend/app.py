import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="Data Dashboard", page_icon="📊")

# Environment variables
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Title
st.title("Data Visualization Dashboard")

# Debug info (only shown if DEBUG is True)
if DEBUG:
    st.sidebar.header("Debug Info")
    st.sidebar.write(f"Backend URL: {BACKEND_URL}")
    st.sidebar.write(f"Debug Mode: {DEBUG}")

# Sidebar
st.sidebar.title("Controls")
selected_view = st.sidebar.selectbox("Select View", ["Data Overview", "Visualization"])

try:
    # Fetch data from backend
    @st.cache_data
    def load_data():
        response = requests.get(f"{BACKEND_URL}/data")
        return pd.DataFrame(response.json())

    if selected_view == "Data Overview":
        st.header("Data Overview")
        data = load_data()
        st.dataframe(data)
        
        st.header("Data Statistics")
        st.write(data.describe())

    elif selected_view == "Visualization":
        st.header("Data Visualization")
        data = load_data()
        
        # Sample visualization
        st.subheader("Sample Chart")
        st.line_chart(data.iloc[:, 1:])

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to backend: {str(e)}")
    if DEBUG:
        st.error(f"Backend URL attempted: {BACKEND_URL}")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    if DEBUG:
        st.exception(e)