FROM python:3.11

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download models during build (optional - can be done at runtime)
RUN python -c "import whisper; whisper.load_model('base')" && \
    python -c "from transformers import pipeline; pipeline('translation', model='Helsinki-NLP/opus-mt-en-es')"

EXPOSE 8000

CMD ["python", "-u", "server.py"]
