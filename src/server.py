from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.webrtc.handler import VoicePipelineOrchestrator

def create_app() -> tuple[FastAPI, VoicePipelineOrchestrator]:
    app = FastAPI(title="Voice Agent WebRTC Service")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    orchestrator = VoicePipelineOrchestrator()
    stream = orchestrator.create_stream()
    
    # Mount FastRTC endpoints on the FastAPI app
    stream.mount(app)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app, stream