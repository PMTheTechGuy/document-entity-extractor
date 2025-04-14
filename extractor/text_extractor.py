# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: This module uses a trained spaCy NER model (or falls back to a default one)
#          to extract names, emails, and organizations from raw text.
# ──────────────────────────────────────────────────────────────────────────────


from dotenv import load_dotenv
from utils.post_process import clean_entities
from pathlib import Path
import logging
import re
import spacy
import os

# Load dev variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Ensure correct path is always passed
PROJECT_ROOT = Path(__file__).resolve().parent.parent


LOG_DIR = PROJECT_ROOT / os.getenv("LOG_DIR")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "text_extractor.log")

file_handler = logging.FileHandler(log_file, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Resolve absolute path to the custom trained model
MODEL_PATH = PROJECT_ROOT / os.getenv("MODEL_PATH")

try:
    nlp = spacy.load(MODEL_PATH)
    logger.info("✅ Loaded custom NER model.")
except Exception as e:
    logger.error("⚠️ Failed to load custom model:", e)
    nlp = spacy.load("en_core_web_sm")
    logger.info("🔁 Falling back to spaCy default model.")


def extract_info(text):
    """
    Extracts person names, email addresses, and organizations from given text.

    Args:
        text (str): The input text to analyze.

    Returns:
        tuple: Lists of (names, emails, organizations)
    """

    logger.info("📝 Starting entity extraction from text.")

    # Extract emails using regex
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)
    logger.info("📧 Found %d email(s).", len(emails))

    # Use spaCy to extract named entities
    doc = nlp(text)
    names = clean_entities([ent.text for ent in doc.ents if ent.label_ == "PERSON"], entity_type="PERSON")
    organizations = clean_entities([ent.text for ent in doc.ents if ent.label_ == "ORG"], entity_type="ORG")

    logger.info(" Extracted %d person name(s) and %d organization(s).", len(names), len(organizations))

    return names, emails, organizations
