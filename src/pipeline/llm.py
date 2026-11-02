import json
from collections.abc import Generator
import httpx
from config.settings import settings

class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    def generate_sentence_stream(self, prompt: str) -> Generator[str, None, None]:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a spoken voice assistant. Keep answers concise (1-2 direct sentences). Never use markdown or emojis.",
                },
                {"role": "user", "content": prompt},
            ],
            "stream": True,
            "options": {"temperature": 0.6, "num_predict": 100}
        }

        sentence_delimiters = {".", "?", "!", "\n"}
        buffer = ""

        with httpx.Client(base_url=self.base_url, timeout=30.0) as client:
            with client.stream("POST", "/api/chat", json=payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    buffer += token

                    if any(punct in token for punct in sentence_delimiters):
                        parts = []
                        last_idx = 0
                        for idx, char in enumerate(buffer):
                            if char in sentence_delimiters:
                                parts.append(buffer[last_idx:idx + 1].strip())
                                last_idx = idx + 1
                        for part in parts:
                            if part:
                                yield part
                        buffer = buffer[last_idx:]

                    if chunk.get("done", False):
                        break

        final_part = buffer.strip()
        if final_part:
            yield final_part