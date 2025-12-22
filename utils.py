import time
import random
import pyperclip
import hashlib
import os
from selenium.webdriver.common.keys import Keys

import json

CHAT_HISTORY_FILE = "logs/chat_history.json"
MAX_HISTORY = 12   # last 12 messages only


def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []

    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_chat_history(history):
    os.makedirs("logs", exist_ok=True)
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-MAX_HISTORY:], f, indent=2)


def add_to_chat_history(role, text):
    history = load_chat_history()
    history.append({
        "role": role,
        "content": text
    })
    save_chat_history(history)

# =========================
# HUMAN DELAY
# =========================

def human_delay(a=0.3, b=1.0):
    time.sleep(random.uniform(a, b))


# =========================
# SEND MESSAGE (PASTE + ENTER ONLY)
# =========================

def paste_and_send(input_box, text):
    pyperclip.copy(text)

    input_box.click()
    time.sleep(0.2)

    input_box.send_keys(Keys.CONTROL, "v")
    time.sleep(0.2)

    input_box.send_keys(Keys.ENTER)


# =========================
# REPLY LOG (HASH BASED)
# =========================

LOG_FILE = "logs/replied_messages.log"


def normalize_text(text: str) -> str:
    return (
        text.replace("\n", " ")
        .replace("Enter", "")
        .strip()
        .lower()
    )


def message_hash(text: str) -> str:
    return hashlib.sha256(
        normalize_text(text).encode("utf-8")
    ).hexdigest()


def has_replied_before(text: str) -> bool:
    if not os.path.exists(LOG_FILE):
        return False

    h = message_hash(text)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return h in f.read()


def save_replied_message(text: str):
    os.makedirs("logs", exist_ok=True)
    h = message_hash(text)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(h + "\n")


# =========================
# LIFECYCLE LOG
# =========================

def log_lifecycle(message: str):
    os.makedirs("logs", exist_ok=True)
    with open("logs/bot_lifecycle.log", "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} - {message}\n")
