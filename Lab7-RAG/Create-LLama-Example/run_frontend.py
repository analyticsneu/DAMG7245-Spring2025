#!/usr/bin/env python
"""
Script to run the Streamlit frontend with the correct Python path.
"""
import os
import subprocess
import sys

def main():
    """Run the Streamlit frontend."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Add the current directory to the Python path
    sys.path.append(script_dir)
    
    # Run the Streamlit app
    frontend_path = os.path.join(script_dir, "frontend", "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", frontend_path], check=True)

if __name__ == "__main__":
    main()
