import numpy as np
from faster_whisper import WhisperModel
from config.settings import settings

class STTService:
    def __init__(self):
        print("[STT] Loading faster-whisper on CPU...")
        self.model = WhisperModel(
            settings.WHISPER_MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        # 1. Flatten from (1, 115200) or (2, N) to 1D (115200,)
        audio_flat = audio_data.squeeze()
        if audio_flat.ndim > 1:
            audio_flat = audio_flat.mean(axis=0)

        # 2. Convert to float32 normalized to [-1.0, 1.0]
        if audio_flat.dtype == np.int16:
            audio_float = audio_flat.astype(np.float32) / 32768.0
        elif audio_flat.dtype == np.float32:
            audio_float = audio_flat
        else:
            audio_float = audio_flat.astype(np.float32)

        # 3. Resample from 48000 Hz to 16000 Hz for Whisper
        if sample_rate != 16000 and len(audio_float) > 0:
            target_samples = int(len(audio_float) * 16000 / sample_rate)
            audio_float = np.interp(
                np.linspace(0, len(audio_float), target_samples, endpoint=False),
                np.arange(len(audio_float)),
                audio_float
            ).astype(np.float32)

        # Ensure contiguous array
        audio_float = np.ascontiguousarray(audio_float)
        print(f"[STT] Transcribing {len(audio_float)} samples at 16000 Hz...")
        segments, info = self.model.transcribe(audio_float, language="en", beam_size=1)
        text = " ".join(seg.text for seg in segments).strip()
        print(f"[STT Result]: '{text}'")
        return text