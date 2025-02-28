from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables with defaults
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

app = FastAPI(
    title="Data API",
    debug=DEBUG,
    root_path=API_PREFIX if APP_ENV == "production" else ""
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generate sample data
def generate_sample_data() -> List[Dict]:
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    data = []
    
    for date in dates:
        record = {
            "date": date.strftime("%Y-%m-%d"),
            "value1": np.random.randint(50, 150),
            "value2": np.random.randint(30, 80)
        }
        data.append(record)
    
    return data

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Data API",
        "environment": APP_ENV,
        "debug_mode": DEBUG
    }

@app.get("/data")
def get_data():
    try:
        data = generate_sample_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": APP_ENV
    }

@app.get("/config")
def get_config():
    """Return non-sensitive configuration information"""
    return {
        "app_env": APP_ENV,
        "debug": DEBUG,
        "api_prefix": API_PREFIX
    }