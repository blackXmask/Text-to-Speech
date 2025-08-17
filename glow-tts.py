from TTS.api import TTS

# Load the model (this will trigger download only)
print("⏳ Downloading 'glow-tts' model for LJSpeech...")
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=True, gpu=False)
print("✅ Model downloaded and cached at:")
print(tts.model_path)
