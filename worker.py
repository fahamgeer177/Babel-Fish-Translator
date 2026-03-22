import whisper
import torch
from transformers import pipeline
from gtts import gTTS
import io
import tempfile
import os
from pydub import AudioSegment
import numpy as np

# Load Whisper model for speech-to-text
# You can use different model sizes: tiny, base, small, medium, large
whisper_model = whisper.load_model("base")  # base model is a good balance of speed and accuracy

# Load translation pipeline using Hugging Face transformers
# Using Helsinki-NLP model for English to Spanish translation
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

def speech_to_text(audio_binary):
    """
    Convert speech audio to text using OpenAI Whisper
    """
    try:
        # Save audio binary to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_binary)
            temp_audio_path = temp_audio.name
        
        # Load and convert audio if needed
        try:
            # Try to load with pydub to handle different audio formats
            audio = AudioSegment.from_file(temp_audio_path)
            # Convert to wav format that Whisper expects
            wav_path = temp_audio_path.replace(temp_audio_path.split('.')[-1], 'wav')
            audio.export(wav_path, format="wav")
            
            # Use Whisper to transcribe
            result = whisper_model.transcribe(wav_path)
            text = result["text"].strip()
            
            print('Whisper transcription result:', text)
            
            # Clean up temporary files
            os.unlink(temp_audio_path)
            if wav_path != temp_audio_path:
                os.unlink(wav_path)
                
            return text if text else "Sorry, I couldn't understand the audio."
            
        except Exception as e:
            print(f"Error processing audio: {e}")
            # Clean up temporary file
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            return "Sorry, I couldn't process the audio."
            
    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        return "Sorry, there was an error processing your speech."

def text_to_speech(text, voice=""):
    """
    Convert text to speech using Google Text-to-Speech (gTTS)
    """
    try:
        # gTTS doesn't support the same voice options as Watson
        # We'll use Spanish for Spanish text, English for English text
        # Detect if text is likely Spanish (simple heuristic)
        spanish_words = ['el', 'la', 'es', 'de', 'en', 'un', 'una', 'con', 'por', 'para', 'que', 'se', 'no', 'te', 'lo', 'le']
        text_lower = text.lower()
        spanish_word_count = sum(1 for word in spanish_words if word in text_lower)
        
        # Choose language based on content
        if spanish_word_count > 2:  # If we find multiple Spanish words
            lang = 'es'
        else:
            lang = 'en'
        
        # Create gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        print(f'Text-to-Speech generated for: "{text}" in language: {lang}')
        return audio_buffer.read()
        
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        # Return empty audio if there's an error
        return b''

def watsonx_process_message(user_message, voice=""):
    """
    Process user message and translate from English to Spanish only if a Spanish voice is selected.
    Otherwise, return the original English message.
    """
    try:
        # List of Spanish voice options from the dropdown (from index.html)
        spanish_voices = [
            "es-ES_LauraV3Voice", "es-LA_SofiaV3Voice", "es-ES_EnriqueV3Voice"
        ]
        # If the user selected a Spanish voice, translate
        if voice in spanish_voices:
            result = translator(user_message)
            translated_text = result[0]['translation_text']
            print("Translation result (Spanish):", translated_text)
            return translated_text
        else:
            print("No translation, returning English:", user_message)
            return user_message
    except Exception as e:
        print(f"Error in translation: {e}")
        return f"Sorry, I couldn't translate: {user_message}"
