import time
import signal
import sys
from datetime import datetime

from browser import launch_browser, open_group_chat
from gc_bot import check_and_reply
from config import BOT_USERNAME


# =========================
# LOGGING
# =========================

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    with open("logs/bot_lifecycle.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


# =========================
# CLEAN SHUTDOWN
# =========================

def shutdown_handler(signal_received=None, frame=None):
    log_event("🛑 Bot shutting down gracefully")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


# =========================
# MAIN
# =========================

def main():
    log_event(f"🤖 Bot starting (@{BOT_USERNAME})")

    print("PHASE 1: Launching browser...")
    driver = launch_browser()
    print("PHASE 1 COMPLETED ✅ Browser opened & logged in")

    print("PHASE 2: Opening Group Chat...")
    open_group_chat(driver)
    print("PHASE 2 COMPLETED ✅ GC loaded")

    print("PHASE 3: Bot is now monitoring messages...")

    try:
        while True:
            check_and_reply(driver)
            time.sleep(3)  # anti-spam / CPU safe

    except Exception as e:
        log_event(f"⚠️ Fatal error: {e}")
        shutdown_handler()


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    main()
