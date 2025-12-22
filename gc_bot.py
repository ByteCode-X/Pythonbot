import time
import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from utils import (
    paste_and_send,
    has_replied_before,
    save_replied_message,
    add_to_chat_history
)
from openrouter_ai import ai_reply
from config import BOT_USERNAME, LOW_PROBABILITY


# =========================
# READ LAST MESSAGES (RAW TEXT)
# =========================

def get_last_messages(driver, limit=5):
    elements = driver.find_elements(
        By.XPATH,
        "//div[@dir='auto']"
    )

    messages = []

    for el in elements:
        try:
            text = el.text.strip()
            if not text:
                continue

            lower = text.lower()

            # noise filters
            if lower in {"you sent", "sent", "seen"}:
                continue
            if "added" in lower or "left" in lower:
                continue
            if len(text) < 2:
                continue

            messages.append(text)

        except StaleElementReferenceException:
            continue

    return messages[-limit:]


# =========================
# INPUT BOX (SEND ONLY)
# =========================

def get_input_box(driver):
    box = driver.find_element(
        By.XPATH,
        "//div[@contenteditable='true']"
    )
    box.click()
    time.sleep(0.3)
    return box


# =========================
# CORE BOT LOOP
# =========================

def check_and_reply(driver):

    print("\n🔍 Checking last messages...")

    try:
        messages = get_last_messages(driver, 5)
    except Exception as e:
        print("⚠️ Failed to read messages:", e)
        return

    if not messages:
        print("ℹ️ No readable messages.")
        return

    print("📜 FINAL LAST 5 MESSAGES:")
    for i, msg in enumerate(messages, 1):
        print(f"  {i}. {msg.splitlines()[0]}")

    # newest → oldest
    for text in reversed(messages):

        if f"@{BOT_USERNAME}" not in text:
            continue

        print(f"\n🟡 Mention detected for @{BOT_USERNAME}")

        # save user message to memory
        add_to_chat_history("user", text)

        if has_replied_before(text):
            print("⏭️ Already replied. Skipping.")
            return

        print("🧠 Sending message to AI...")
        reply = ai_reply(text)

        if not reply:
            print("⚠️ AI failed.")
            return

        print("🤖 AI reply:")
        print(f"👉 {reply}")

        try:
            input_box = get_input_box(driver)
            paste_and_send(input_box, reply)

            add_to_chat_history("assistant", reply)
            save_replied_message(text)

            print("✅ Reply sent & logged")

        except Exception as e:
            print("⚠️ Send failed:", e)

        return

    # =========================
    # RANDOM MESSAGE (LOW PROBABILITY)
    # =========================

    if random.random() < LOW_PROBABILITY:
        print("\n🎲 Random message triggered")

        reply = ai_reply(
            "Say something casual, short and friendly in a group chat"
        )

        if reply:
            try:
                input_box = get_input_box(driver)
                paste_and_send(input_box, reply)
                add_to_chat_history("assistant", reply)
                print("✅ Random message sent")
            except Exception as e:
                print("⚠️ Random send failed:", e)
