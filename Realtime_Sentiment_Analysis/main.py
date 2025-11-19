# main.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import whisper
import torch
import numpy as np
import librosa
from transformers import pipeline

# -----------------------------
# 1️⃣ Load Models
# -----------------------------
st.title("🎤 Real-Time Speech Emotion and Sentiment Analysis")

# Whisper model for speech-to-text
st.info("Loading Whisper model...")
whisper_model = whisper.load_model("base")  

# Text-based sentiment analysis model
st.info("Loading sentiment analysis model...")
sentiment_analyzer = pipeline("sentiment-analysis")

# -----------------------------
# 2️⃣ WebRTC Microphone Streaming
# -----------------------------
class AudioProcessor(AudioProcessorBase):
    """
    This class processes audio frames from the microphone in real-time.
    Each audio frame is appended to a buffer for later analysis.
    """
    def __init__(self):
        self.buffer = []

    def recv(self, frame):
        # Convert audio frame to numpy array
        audio = frame.to_ndarray()
        # Append the audio data to buffer
        self.buffer.append(audio)
        return frame

def process_audio(buffer):
    """
    Convert audio buffer to a format suitable for analysis,
    run speech-to-text with Whisper, and analyze text sentiment.
    """
    # Concatenate all buffered audio frames
    audio_np = np.concatenate(buffer, axis=0)
    
    # Normalize audio to float32 [-1, 1]
    audio_float = audio_np.astype(np.float32) / 32768.0

    # Sample rate (Whisper expects 16kHz)
    sr = 16000

    # -----------------------------
    # 3️⃣ Speech-to-Text (Whisper)
    # -----------------------------
    result = whisper_model.transcribe(audio_float, fp16=False, language="en")
    text = result['text']

    # -----------------------------
    # 4️⃣ Text Sentiment Analysis
    # -----------------------------
    sentiment = sentiment_analyzer(text)[0]  # Example: {'label': 'POSITIVE', 'score': 0.99}

    # -----------------------------
    # 5️⃣ Voice Feature Extraction (Optional)
    # -----------------------------
    # Compute Mel-spectrogram to later feed a voice emotion classifier
    mel_spec = librosa.feature.melspectrogram(y=audio_float, sr=sr, n_mels=128)
    
    return text, sentiment, mel_spec

# -----------------------------
# 6️⃣ Streamlit UI
# -----------------------------
st.write("Click 'Start' to begin microphone streaming.")
webrtc_ctx = webrtc_streamer(key="speech-analysis", audio_processor_factory=AudioProcessor)

# Once audio is collected, process it
if webrtc_ctx.audio_processor:
    if st.button("Analyze"):
        buffer = webrtc_ctx.audio_processor.buffer
        if buffer:
            text, sentiment, mel_spec = process_audio(buffer)
            st.subheader("Transcribed Text")
            st.write(text)

            st.subheader("Text Sentiment")
            st.write(f"{sentiment['label']} ({sentiment['score']:.2f})")

            st.subheader("Mel-Spectrogram (Audio Features)")
            st.line_chart(np.mean(mel_spec, axis=0))
        else:
            st.warning("No audio data collected yet.")
