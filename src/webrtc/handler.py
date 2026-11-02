import numpy as np
from collections.abc import Generator
from fastrtc import Stream, ReplyOnPause
from src.pipeline.stt import STTService
from src.pipeline.llm import LLMService
from src.pipeline.tts import TTSService
from src.automation.n8n_client import trigger_n8n_flow

class VoicePipelineOrchestrator:
    def __init__(self):
        self.stt = STTService()
        self.llm = LLMService()
        self.tts = TTSService()

    def handle_voice_turn(self, audio: tuple[int, np.ndarray]) -> Generator[tuple[int, np.ndarray], None, None]:
        sample_rate, audio_data = audio
        print(f"\n[VAD Triggered] Shape={audio_data.shape}, SampleRate={sample_rate}")

        # 1. Transcribe audio
        user_prompt = self.stt.transcribe(audio_data, sample_rate)
        if not user_prompt:
            return

        print(f"\n[User Prompt]: {user_prompt}")
        print("[Assistant]: ", end="", flush=True)

        full_reply_parts = []
        try:
            for sentence in self.llm.generate_sentence_stream(user_prompt):
                print(f"{sentence} ", end="", flush=True)
                full_reply_parts.append(sentence)
                yield from self.tts.stream_audio(sentence)
        except Exception as e:
            print(f"\n[LLM/TTS Error]: {e}")

        print()

        # 3. Parallel Background Automation (fired safely via daemon thread)
        if full_reply_parts:
            full_reply = " ".join(full_reply_parts)
            trigger_n8n_flow(user_prompt, full_reply)

    def create_stream(self) -> Stream:
        return Stream(
            handler=ReplyOnPause(
                self.handle_voice_turn,
                can_interrupt=True
            ),
            modality="audio",
            mode="send-receive"
        )