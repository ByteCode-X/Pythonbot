import os
import time
import requests
from dotenv import load_dotenv

from utils import load_chat_history

# =========================
# ENV
# =========================

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ OPENROUTER_API_KEY not found in .env")

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://localhost",
    "X-Title": "Instagram Group Bot"
}

# =========================
# AI FUNCTION
# =========================

def ai_reply(prompt, retries=3):
    history = load_chat_history()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a smart, friendly Instagram group chat bot. "
                "Reply short, natural, and human-like. "
                "Avoid repeating answers. Emojis allowed but minimal. "
                "Sometimes be playful or thoughtful."
            )
        }
    ]

    # Add memory
    messages.extend(history)

    # Current message
    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.85,
        "max_tokens": 120
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            return response.json()["choices"][0]["message"]["content"].strip()

        except Exception as e:
            print(f"⚠️ OpenRouter error {attempt}/{retries}:", e)
            time.sleep(2)

    return None

