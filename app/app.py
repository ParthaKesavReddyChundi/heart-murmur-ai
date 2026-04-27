import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import tempfile

from src.utils.inference import predict

st.title("💓 Heart Murmur Detection System")

st.write("Upload a heart sound (.wav) file to analyze.")

# Upload file
uploaded_file = st.file_uploader("Choose a .wav file", type=["wav"])

if uploaded_file is not None:
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    # Load audio
    signal, sr = librosa.load(file_path, sr=4000)

    st.subheader("📊 Waveform")
    fig, ax = plt.subplots()
    librosa.display.waveshow(signal, sr=sr, ax=ax)
    st.pyplot(fig)

    # Prediction
    st.subheader("🔍 Analysis Result")

    pred, prob = predict(file_path)

    st.metric(label="Murmur Probability", value=f"{prob:.4f}")

    if prob > 0.6:
        st.error("🔴 High Risk: Murmur Detected - Immediate medical consultation recommended")
    elif prob > 0.45:
        st.warning("🟠 Moderate Risk: Possible murmur detected - Further evaluation advised")
    else:
        st.success("🟢 Low Risk: Normal heart sound")

    st.write(f"### Final Prediction: {pred}")

    if pred == "Murmur":
        st.error("⚠️ Murmur Detected - Please consult a doctor")
    else:
        st.success("✅ Normal Heart Sound")