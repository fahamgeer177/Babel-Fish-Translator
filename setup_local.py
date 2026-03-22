#!/usr/bin/env python3
"""
Setup script for Babel Fish Translator with OpenAI Whisper
This script will help you set up the project with local AI models
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def download_whisper_model():
    """Download Whisper model"""
    print("Downloading Whisper base model (this may take a few minutes)...")
    try:
        import whisper
        model = whisper.load_model("base")
        print("✅ Whisper model downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading Whisper model: {e}")
        return False

def download_translation_model():
    """Download translation model"""
    print("Downloading translation model...")
    try:
        from transformers import pipeline
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")
        print("✅ Translation model downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading translation model: {e}")
        return False

def main():
    print("🚀 Setting up Babel Fish Translator with Local AI Models")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed at requirements installation.")
        return
    
    # Download models
    if not download_whisper_model():
        print("Setup failed at Whisper model download.")
        return
        
    if not download_translation_model():
        print("Setup failed at translation model download.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  python server.py")
    print("\nThen open your browser to: http://localhost:8000")
    print("\nNote: The first time you use speech recognition, it may take a moment to load the models.")

if __name__ == "__main__":
    main()
