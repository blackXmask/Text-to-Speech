import streamlit as st
from TTS.api import TTS
import tempfile
import os
import json

# --- Streamlit setup ---
st.set_page_config(page_title="🔊 Label TTS Speakers", layout="centered")
st.title("🎧 Coqui TTS Speaker Labeling Tool (VCTK Model)")

# --- Load TTS model ---
@st.cache_resource
def load_model():
    return TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

tts = load_model()
sample_text = "This is a sample voice demo for labeling this speaker."

# --- Load or initialize label file ---
LABELS_FILE = "speaker_labels.json"
if os.path.exists(LABELS_FILE):
    with open(LABELS_FILE, "r") as f:
        labels = json.load(f)
else:
    labels = {}

# --- Speaker selector ---
speaker_ids = tts.speakers
index = st.number_input("🎙 Speaker Index", 0, len(speaker_ids) - 1, step=1)
current_speaker = speaker_ids[index]
st.markdown(f"**Current speaker ID:** `{current_speaker}`")

# --- Audio generation ---
if st.button("▶️ Generate Voice Preview"):
    with st.spinner(f"🔄 Generating voice for {current_speaker}..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            try:
                tts.tts_to_file(text=sample_text, speaker=current_speaker, file_path=fp.name)
                st.audio(fp.name, format="audio/wav")
            except Exception as e:
                st.error(f"❌ Error generating voice: {e}")

# --- Label input and save ---
label = st.text_input("✏️ Enter a meaningful label", value=labels.get(current_speaker, ""))
if st.button("💾 Save Label"):
    labels[current_speaker] = label
    with open(LABELS_FILE, "w") as f:
        json.dump(labels, f, indent=2)
    st.success(f"✅ Label saved for `{current_speaker}`")
