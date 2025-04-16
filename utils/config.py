import os
from dotenv import load_dotenv

load_dotenv()

def use_gpt_extraction():
    return os.getenv("USE_GPT_EXTRACTION", "False").lower() == "true"
