# services/audio_service.py
import whisper
import io
import torch

# load small whisper model (faster)
model = whisper.load_model("small")  # or "tiny" for speed

def transcribe_audio_bytes(audio_bytes: bytes, language="en"):
    with io.BytesIO(audio_bytes) as f:
        f.seek(0)
        # whisper requires file path or bytes-like; we save to temp
        import tempfile
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(f.read())
        tmp.flush()
        tmp.close()
        result = model.transcribe(tmp.name, language=language)
        return result.get("text", "")
