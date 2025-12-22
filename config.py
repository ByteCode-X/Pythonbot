# ===== This is the Configuration for the Instagram Bot ===================================================
# It is actually connected to the .env file for sensitive information.
# The bot uses GPT-4o-mini by default, but you can change it to any other model supported by OpenRouter.
# ===================================================================================================================

import os
from dotenv import load_dotenv


load_dotenv()

SESSION_ID = os.getenv("SESSION_ID")

BOT_USERNAME = os.getenv("BOT_USERNAME")
GC_URL = os.getenv("GC_URL")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "openai/gpt-4o-mini" 

LOW_PROBABILITY = float(os.getenv("LOW_PROBABILITY", 0.03))
CHECK_DELAY = 6

