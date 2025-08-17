import streamlit as st
from TTS.api import TTS
from deep_translator import GoogleTranslator
import tempfile, os
from pydub import AudioSegment
import whisper

# --- UI Setup ---
st.set_page_config(page_title="Neural TTS Studio", layout="wide", page_icon="🎙️")

# --- Custom Animated CSS ---
st.markdown("""
<style>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
html, body {
    background: linear-gradient(135deg, #0f0f1e, #1a1a2e);
    color: #e0e0ff;
    font-family: 'Segoe UI', sans-serif;
    animation: fadeIn 1.5s ease-in;
}
h1, h3 {
    background: linear-gradient(90deg, #00ffff, #0066ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeInUp 1s ease-in-out;
}
textarea, .stTextInput > div > div > input {
    font-size: 16px !important;
    color: #00ffff;
    background-color: #111122;
    border: 1px solid #00ffff40;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 0 10px #00ffff40;
    transition: all 0.3s ease;
}
textarea:focus, .stTextInput > div > div > input:focus {
    outline: none;
    box-shadow: 0 0 15px #00ffff;
    border-color: #00ffff;
}
.stSelectbox select, .stSlider, .stCheckbox > label {
    color: #c2f0f7;
}
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    font-size: 16px;
    font-weight: 600;
    padding: 0.8rem 1.2rem;
    border: none;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, background 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #1e40af, #0a2563);
    transform: scale(1.03);
}
.right-panel-scroll {
    max-height: 85vh;
    overflow-y: auto;
    padding: 1rem;
    margin-left: 1rem;
    background-color: #0f0f1e;
    border-radius: 12px;
    box-shadow: 0 0 15px #00ffff55;
    animation: fadeInUp 1s ease;
}
.right-panel-scroll::-webkit-scrollbar {
    width: 8px;
}
.right-panel-scroll::-webkit-scrollbar-track {
    background: transparent;
}
.right-panel-scroll::-webkit-scrollbar-thumb {
    background-color: #00ffff55;
    border-radius: 10px;
}
.upload-button, .delete-button {
    width: 100%;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    border: none;
    cursor: pointer;
    transition: background 0.3s ease;
}
.upload-button {
    background-color: #088f8f;
    color: white;
}
.upload-button:hover {
    background-color: #055757;
}
.delete-button {
    background-color: #bb2525;
    color: white;
}
.delete-button:hover {
    background-color: #7a1717;
}
.saved-voice-row {
    background: #181835;
    padding: 0.6rem 1rem;
    border-radius: 10px;
    margin-bottom: 0.8rem;
    box-shadow: 0 0 8px #00ffff30;
    display: flex;
    align-items: center;
    justify-content: space-between;
    animation: fadeInUp 0.8s ease;
}
.saved-voice-info {
    color: #b0f0f7;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)

# --- Load Models ---
@st.cache_resource
def load_tts_model():
    return TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

@st.cache_resource
def load_stt_model():
    return whisper.load_model("base")

tts = load_tts_model()
stt = load_stt_model()

# --- Speaker Setup ---
speakers = tts.speakers
voices = [f"Voice-{i+1:02}" for i in range(len(speakers))]
lookup = {f"Voice-{i+1:02}": sid for i, sid in enumerate(speakers)}
voices.insert(0, "Default Voice")
lookup["Default Voice"] = speakers[0]

# --- Session State ---
for key in ["prev_text", "prev_voice", "orig", "generation_started"]:
    if key not in st.session_state:
        st.session_state[key] = "" if "text" in key or "voice" in key else None

# --- Enhanced Echo ---
def apply_echo(audio: AudioSegment, repeats=3, delay_ms=200, decay_db=6):
    output = audio
    for i in range(1, repeats + 1):
        attenuated = audio - decay_db * i
        output = output.overlay(attenuated, position=delay_ms * i)
    return output

# === MAIN ===
st.title("🎙 Neural TTS Studio")
st.markdown("#### 🔊 Translate → Generate Voice → Tweak Audio")

text = st.text_area("💬 Enter text (any language):", height=150, key="input_text")

st.sidebar.header("🎛 TTS Voice Settings")
voice = st.sidebar.selectbox("🎙 Voice", voices, key="voice")
gain = st.sidebar.slider("🔊 Volume (dB)", -20, 20, 3)
pitch = st.sidebar.slider("🎚 Pitch (semitones)", -12, 12, 1)
speed = st.sidebar.slider("⏩ Speed", 0.5, 2.0, 0.95, 0.05)
echo = st.sidebar.checkbox("🎧 Add Echo")

def regenerate_audio():
    try:
        translated = GoogleTranslator(source="auto", target="en").translate(st.session_state.input_text)
    except:
        translated = st.session_state.input_text

    sid = lookup[st.session_state.voice]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tts.tts_to_file(text=translated, speaker=sid, file_path=tmp.name)
    st.session_state.orig = tmp.name
    st.session_state.prev_text = st.session_state.input_text
    st.session_state.prev_voice = st.session_state.voice

if st.button("🔊 Generate Voice"):
    if st.session_state.input_text.strip():
        with st.spinner("🔁 Generating..."):
            regenerate_audio()
            st.session_state.generation_started = True
    else:
        st.warning("⚠️ Please enter some text before generating.")

if st.session_state.generation_started and st.session_state.input_text.strip():
    if (st.session_state.input_text != st.session_state.prev_text or
        st.session_state.voice != st.session_state.prev_voice):
        with st.spinner("🔁 Updating voice..."):
            regenerate_audio()

if st.session_state.orig:
    try:
        audio = AudioSegment.from_wav(st.session_state.orig) + gain
        if pitch:
            fr = int(audio.frame_rate * (2 ** (pitch / 12)))
            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": fr}).set_frame_rate(22050)
        if speed != 1:
            audio = audio._spawn(audio.raw_data).set_frame_rate(int(audio.frame_rate * speed))
        if echo:
            audio = apply_echo(audio)

        tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(tmp2.name, format="wav")

        st.audio(tmp2.name)
        with open(tmp2.name, "rb") as f:
            st.download_button("⬇️ Download Audio", f, "output.wav", "audio/wav")
    except Exception as e:
        st.error(f"❌ Audio processing failed: {e}")

# === SIDEBAR: Speech-to-Text + Uploaded Voices ===
st.sidebar.subheader("🗣️ Speech to Text (Whisper)")
audio_file = st.sidebar.file_uploader("🎤 Upload audio (.wav)", type=["wav"])
if audio_file:
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp.write(audio_file.read())
    temp.close()

    if st.sidebar.button("📝 Transcribe Audio"):
        with st.spinner("🧠 Transcribing..."):
            result = stt.transcribe(temp.name)
            st.sidebar.success("✅ Transcription Complete")
            st.sidebar.text_area("📋 Transcribed Text:", value=result["text"], height=100)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Uploaded Voices")
upload_dir = "uploaded_voices"
os.makedirs(upload_dir, exist_ok=True)
saved = [f for f in os.listdir(upload_dir) if f.endswith(".wav")]

playback_gain = st.sidebar.slider("Gain (dB)", -10, 10, 3, key="upload_gain")
playback_speed = st.sidebar.slider("Speed", 0.5, 2.0, 0.95, 0.05, key="upload_speed")
playback_pitch = st.sidebar.slider("Pitch", -12, 12, 0, key="upload_pitch")
playback_echo = st.sidebar.checkbox("Add Echo", key="upload_echo")

uploaded = st.sidebar.file_uploader("📂 Upload Voice Sample (.wav)", type=["wav"], key="voice_upload")
custom_name = st.sidebar.text_input("📝 Name this voice:")

if st.sidebar.button("💾 Save Voice", key="save_voice_btn"):
    if uploaded and custom_name.strip():
        path = os.path.join(upload_dir, f"{custom_name.strip().replace(' ', '_')}.wav")
        with open(path, "wb") as f:
            f.write(uploaded.read())
        st.sidebar.success(f"✅ Saved as: {custom_name.strip()}.wav")
    else:
        st.sidebar.warning("⚠️ Upload a file and enter a name to save.")

for file in saved:
    try:
        audio_path = os.path.join(upload_dir, file)
        audio = AudioSegment.from_wav(audio_path) + playback_gain
        if playback_pitch != 0:
            fr = int(audio.frame_rate * (2 ** (playback_pitch / 12)))
            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": fr}).set_frame_rate(22050)
        if playback_speed != 1:
            audio = audio._spawn(audio.raw_data).set_frame_rate(int(audio.frame_rate * playback_speed))
        if playback_echo:
            audio = apply_echo(audio)

        tmp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(tmp3.name, format="wav")

        st.sidebar.audio(tmp3.name)
        st.sidebar.markdown(f"🎧 `{file.replace('_', ' ').replace('.wav', '')}`")
        if st.sidebar.button("🗑 Delete", key=f"del_{file}"):
            os.remove(audio_path)
            st.experimental_rerun()
    except Exception as e:
        st.sidebar.warning(f"⚠️ Could not load {file} | {e}")
