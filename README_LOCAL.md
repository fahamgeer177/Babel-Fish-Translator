# Babel Fish Translator - Local AI Version

A voice-powered English to Spanish translator using local AI models instead of IBM Watson services.

## Features

- **Speech-to-Text**: OpenAI Whisper (runs locally)
- **Translation**: Helsinki-NLP English-Spanish model (via Hugging Face)
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Web Interface**: Modern responsive UI with microphone recording

## Quick Start

### Option 1: Automatic Setup (Recommended)

1. Run the setup script:
```bash
python setup_local.py
```

2. Start the server:
```bash
python server.py
```

3. Open your browser to: http://localhost:8000

### Option 2: Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python server.py
```

### Option 3: Docker

```bash
docker build -t babel-fish-translator .
docker run -p 8000:8000 babel-fish-translator
```

## How It Works

1. **Record Audio**: Click the microphone button to record your English speech
2. **Speech Recognition**: Whisper converts your speech to text
3. **Translation**: Helsinki-NLP model translates English to Spanish
4. **Speech Synthesis**: gTTS converts the Spanish text back to speech

## Model Information

- **Whisper Model**: `base` (39 MB) - Good balance of speed and accuracy
  - Other options: `tiny` (39 MB, fastest), `small` (244 MB), `medium` (769 MB), `large` (1550 MB, most accurate)
- **Translation Model**: Helsinki-NLP/opus-mt-en-es (298 MB)
- **TTS**: Google Text-to-Speech (online service, free)

## System Requirements

- Python 3.8+
- ~1GB disk space for models
- Internet connection (for gTTS and model downloads)
- Microphone access in browser

## Troubleshooting

### Common Issues:

1. **Audio not working**: Ensure your browser has microphone permissions
2. **Models downloading slowly**: First run may take time to download models
3. **Memory issues**: Use smaller Whisper model (`tiny` instead of `base`)

### Changing Whisper Model Size:

Edit `worker.py` line 11:
```python
whisper_model = whisper.load_model("tiny")  # or "small", "medium", "large"
```

## Advantages Over IBM Watson Version

- ✅ **Free**: No API costs or usage limits
- ✅ **Private**: All processing happens locally (except gTTS)
- ✅ **Offline-capable**: Speech recognition and translation work offline
- ✅ **No API keys**: No setup of external services required
- ✅ **Customizable**: Can easily swap models or add languages

## Future Enhancements

- Add more language pairs
- Implement fully offline TTS
- Add real-time streaming recognition
- Support for multiple file formats
- Add conversation history

## License

MIT License - Feel free to use and modify!
