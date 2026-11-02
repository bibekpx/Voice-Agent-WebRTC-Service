import numpy as np
from collections.abc import Generator
from fastrtc import get_tts_model

class TTSService:
    def __init__(self):
        print("[TTS] Initializing Kokoro TTS engine...")
        self.tts_model = get_tts_model()

    def stream_audio(self, text: str) -> Generator[tuple[int, np.ndarray], None, None]:
        cleaned_text = text.strip()
        if not cleaned_text:
            return

        print(f"\n[TTS Synthesizing]: '{cleaned_text[:40]}...'")
        try:
            # .tts() returns (sample_rate, np.ndarray)
            sample_rate, audio_data = self.tts_model.tts(cleaned_text)
            
            audio_data = np.ascontiguousarray(audio_data)
            yield (sample_rate, audio_data)
        except Exception as e:
            print(f"[TTS Error]: {e}")