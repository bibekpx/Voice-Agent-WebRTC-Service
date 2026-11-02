🎙️ Local Real-Time Voice Agent (WebRTC + Whisper + Ollama + Kokoro TTS)

Hey there! 👋 Welcome to the Voice Agent WebRTC Service repository.

This project is a 100% local, low-latency, full-duplex voice assistant built in Python. You speak into your browser mic, and it talks right back—with support for real-time interruptions (barge-in) and background webhook logging to n8n.

No complicated cloud APIs required. Everything runs locally on your machine.

⚡ How It Works (The Simple Flow)

Every time you speak and pause, the app runs a fast 4-step relay race:

🎤 [Your Browser Mic]
       │
       ▼  (WebRTC Audio + Voice Activity Detection via FastRTC)
🧠 1. handler.py (The Orchestrator) ──► Detects when you pause speaking
       │
       ├──► 👂 2. stt.py (The Ears)  ──► Resamples audio to 16kHz & transcribes text (Faster-Whisper)
       │
       ├──► 💬 3. llm.py (The Brain) ──► Streams words from Ollama & slices complete sentences
       │
       ├──► 🔊 4. tts.py (The Voice) ──► Speaks each sentence immediately as it arrives (Kokoro TTS)
       │
       └──► 🔗 5. n8n_client.py      ──► Logs the chat in a background thread (Zero lag!)


Why is it so fast?

Instead of waiting for the LLM to write a whole paragraph before speaking, llm.py streams tokens and cuts them as soon as it sees a ., ?, or !. While you are listening to Sentence 1, the AI is already generating Sentence 2.

📂 Project Structure

├── main.py                      # 🚀 Entry point (starts the WebRTC UI on port 7860)
├── config/
│   └── settings.py              # ⚙️ Model names, URLs, and environment variables
└── src/
    ├── server.py                # 🌐 FastAPI server setup, CORS, and /health route
    ├── webrtc/
    │   └── handler.py           # 🎛️ Main voice loop (connects STT -> LLM -> TTS -> n8n)
    ├── pipeline/
    │   ├── stt.py               # 👂 Faster-Whisper Speech-to-Text (CPU int8)
    │   ├── llm.py               # 💬 Ollama streaming client & sentence splitter
    │   └── tts.py               # 🔊 Kokoro Text-to-Speech audio generator
    └── automation/
        └── n8n_client.py        # 🔗 Non-blocking background webhook sender


🚀 Quick Start (Get Running in 2 Minutes)

1. Prerequisites

Python 3.10+

Ollama installed and running locally. Pull a fast model:

ollama pull llama3.2


2. Install Dependencies

pip install -r requirements.txt


3. Check Your Settings (config/settings.py)

Make sure your config/settings.py (or .env) has your local setup configured:

Setting

Example

What it does

WHISPER_MODEL_SIZE

"base.en"

Whisper model size (tiny.en, base.en, small)

OLLAMA_BASE_URL

"http://localhost:11434"

Where your local Ollama server is running

OLLAMA_MODEL

"llama3.2"

The Ollama model used to reply

N8N_WEBHOOK_URL

""

(Optional) Your n8n webhook URL for logging chats

4. Run the App!

Option A: Launch with the built-in Browser Test UI (Recommended for dev)

python main.py


👉 Open http://localhost:7860 in your browser, allow microphone access, and start talking!

Option B: Run as a pure FastAPI Backend (For custom React/Next.js frontends)

uvicorn main:app --host 0.0.0.0 --port 8000 --reload


👉 Health check available at: GET http://localhost:8000/health

🛠️ Developer Cheat Sheet ("Where Do I Edit...?")

Jumping into the code? Here is exactly where to look when making changes:

If you want to...

Open this file

Look at this function

Change the AI's personality or prompt

src/pipeline/llm.py

generate_sentence_stream() (Edit the "system" message)

Switch Whisper from CPU to GPU (CUDA)

src/pipeline/stt.py

__init__() (Change device="cpu" to device="cuda")

Tweak TTS voice synthesis

src/pipeline/tts.py

stream_audio() (self.tts_model.tts(...))

Add new FastAPI routes

src/server.py

create_app() (Add your @app.get / @app.post routes)

Customize the n8n webhook JSON

src/automation/n8n_client.py

_send_webhook_sync() (Edit the payload dictionary)

Disable/Enable voice interruption

src/webrtc/handler.py

create_stream() (ReplyOnPause(..., can_interrupt=True))

🔍 Function-by-Function Call Flow (For Debugging)

When you speak into the mic and pause, here is the exact chain of functions that fire:

VoicePipelineOrchestrator.handle_voice_turn(audio) (in src/webrtc/handler.py)

Receives (sample_rate, audio_data) from FastRTC when you stop talking.

STTService.transcribe(audio_data, sample_rate) (in src/pipeline/stt.py)

Flattens stereo to mono $\rightarrow$ normalizes int16 to float32 $\rightarrow$ resamples 48000Hz to 16000Hz $\rightarrow$ runs faster-whisper and returns user_prompt.

LLMService.generate_sentence_stream(user_prompt) (in src/pipeline/llm.py)

Streams tokens from Ollama's /api/chat and yields one finished sentence at a time.

TTSService.stream_audio(sentence) (in src/pipeline/tts.py)

Converts each sentence into a (sample_rate, audio_data) waveform and streams it immediately to your speakers.

trigger_n8n_flow(user_prompt, full_reply) (in src/automation/n8n_client.py)

Spawns a background daemon thread (_send_webhook_sync) to POST the conversation to n8n so the voice loop never freezes.

⚠️ 3 Golden Rules Before You git push

Never block the main voice loop: If you add database calls or external API requests, always run them in a background thread (like n8n_client.py does) so the audio stream never stutters.

Keep np.ascontiguousarray() in STT & TTS: Both faster-whisper and fastrtc rely on C-contiguous NumPy arrays. Removing those lines can cause memory errors or garbled audio.

No Markdown or Emojis in the LLM System Prompt: Keep the system prompt strict—otherwise the TTS engine will literally say "asterisk asterisk" out loud!"# Voice-Agent-WebRTC-Service" 
"# Voice-Agent-WebRTC-Service" 
"# Voice-Agent-WebRTC-Service" 
"# Voice-Agent-WebRTC-Service" 
"# Voice-Agent-WebRTC-Service" 
"# Voice-Agent-WebRTC-Service" 
"# Voice-Agent-WebRTC-Service" 
"# Voice-Agent-WebRTC-Service" 
