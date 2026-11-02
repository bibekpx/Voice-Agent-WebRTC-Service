from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WHISPER_MODEL_SIZE: str = "base.en"
    WHISPER_DEVICE: str = "cuda"       
    WHISPER_COMPUTE_TYPE: str = "int8"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    N8N_WEBHOOK_URL: str = ""         
    class Config:
        env_file = ".env"

settings = Settings()