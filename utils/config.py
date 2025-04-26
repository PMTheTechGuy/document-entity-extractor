# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Manages the environment variable that allows switching between the SpaCy model and the OpenAI model (using an API key).
# ──────────────────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv

load_dotenv()

def use_gpt_extraction():
    return os.getenv("USE_GPT_EXTRACTION", "False").lower() == "true"
