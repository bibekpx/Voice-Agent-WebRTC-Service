import threading
import httpx
from config.settings import settings

def _send_webhook_sync(user_text: str, agent_text: str) -> None:
    if not settings.N8N_WEBHOOK_URL:
        return

    payload = {
        "event": "voice_interaction_completed",
        "user_query": user_text,
        "assistant_response": agent_text
    }

    try:
        httpx.post(settings.N8N_WEBHOOK_URL, json=payload, timeout=4.0)
    except Exception as err:
        print(f"[Automation Warning] Webhook call failed: {err}")

def trigger_n8n_flow(user_text: str, agent_text: str) -> None:
    """Dispatches webhook non-blockingly without relying on an active asyncio loop."""
    if not settings.N8N_WEBHOOK_URL:
        return
    threading.Thread(target=_send_webhook_sync, args=(user_text, agent_text), daemon=True).start()