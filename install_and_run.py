#!/usr/bin/env python3
"""
Installation and setup script for Diamond Price Prediction App
This script will install all required dependencies and run the app.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(" All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error installing packages: {e}")
        return False

def train_model():
    """Train the machine learning model"""
    print("🤖 Training the machine learning model...")
    try:
        subprocess.check_call([sys.executable, "train_model.py"])
        print("Model trained successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error training model: {e}")
        return False

def run_app():

    print(" Starting the Diamond Price Prediction App...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n App stopped by user")
    except Exception as e:
        print(f" Error running app: {e}")

def main():
    """Main installation and setup process"""
    print("💎 Diamond Price Prediction App - Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("diamonds.csv"):
        print("Error: diamonds.csv not found. Please run this script from the project directory.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Train model
    if not train_model():
        return
    
    print("\n Setup complete! The app will now start...")
    print(" The app will open in your default web browser")
    print("If it doesn't open automatically, go to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the app when you're done.\n")
    
    # Run the app
    run_app()

if __name__ == "__main__":
    main()

