# Instagram Group Chat Automation Bot 🤖

A Python-based automation bot for Instagram group chats that uses **Selenium** for browser automation and **OpenRouter AI** for intelligent, human-like replies.
The bot monitors group messages, responds to mentions, maintains chat context, avoids duplicate replies.

---

## 📌 Features

- ✅ Automated Instagram login using **session ID**
- 💬 Reads latest group chat messages (raw text, emoji-safe)
- 🤖 AI-powered replies via **OpenRouter API**
- 🎲 Random casual messages (low probability)
- ⌨️ Human-like sending using **clipboard + ENTER**
- 📝 Lifecycle logging (bot start/stop)
- 🗂️ Structured, modular codebase
- 🔒 `.env`-based configuration (secure)

---

## 📁 Project Structure

```
Pythonbot/
│
├── bot.py                 # Main entry point
├── gc_bot.py              # Group chat logic
├── browser.py             # Browser & session handling
├── openrouter_ai.py       # AI integration
├── utils.py               # Utilities (logs, delays, memory)
├── .env                   # Sensitive Information
├── config.py              # Environment variable loader
│
├── logs/
│   ├── replied_messages.log
│   ├── chat_history.json
│   └── bot_lifecycle.log
│
├── data/
├── 
└── README.md
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
SESSION_ID=your_instagram_session_id
OPENROUTER_API_KEY=your_openrouter_api_key
BOT_USERNAME=slayergojo.bot
GC_URL=https://www.instagram.com/direct/t/XXXXXXXX/
LOW_PROBABILITY=0.05
```

⚠️ Never commit your `.env` file.

---

## 📦 Dependencies

```bash
pip install selenium webdriver-manager python-dotenv pyperclip requests
```

---

## 🚀 How to Run

```bash
python bot.py
```

---

## 🧠 Chat Memory

- Stored in `logs/chat_history.json`
- Keeps last 12 messages
- Used to improve AI replies
- Auto-resets if corrupted

---

## ⚠️ Disclaimer

This project is for educational purposes only.
Automating Instagram may violate its Terms of Service.
Use at your own risk.

---

## 👤 Author

Developed by **Niraj**
A Coding Enthusiast !
