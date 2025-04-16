# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Extract PERSON, ORG, EMAIL from text using custom spaCy NER model or GPT.
# ──────────────────────────────────────────────────────────────────────────────

import os
import re
import logging
import spacy
from dotenv import load_dotenv
from pathlib import Path

from utils.config import use_gpt_extraction
from utils.post_process import clean_entities
from gpt_integration.gpt_extractor import extract_entities_with_gpt

# Load .env variables
load_dotenv()

# ─────── Setup Logging ───────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / os.getenv("LOG_DIR", "logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / "text_extractor.log"
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
logger.addHandler(file_handler)

# ─────── Load spaCy model ───────
MODEL_PATH = PROJECT_ROOT / os.getenv("MODEL_PATH", "training/custom_ner_model")

try:
    nlp = spacy.load(MODEL_PATH)
    logger.info("✅ Loaded custom NER model from %s", MODEL_PATH)
except Exception:
    logger.exception("⚠️ Failed to load custom model. Falling back to default.")
    nlp = spacy.load("en_core_web_sm")
    logger.info("🔁 Loaded spaCy default model.")


def extract_info_spacy(text: str) -> tuple[list[str], list[str], list[str]]:
    """
    Extract entities using spaCy.
    Returns: (names, emails, organizations)
    """
    logger.info("📝 Starting entity extraction from text.")

    # Emails via regex
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)
    logger.info("📧 Found %d email(s).", len(emails))

    # Named entity recognition
    doc = nlp(text)
    names = clean_entities([ent.text for ent in doc.ents if ent.label_ == "PERSON"], entity_type="PERSON")
    orgs = clean_entities([ent.text for ent in doc.ents if ent.label_ == "ORG"], entity_type="ORG")

    logger.info("✅ Extracted %d name(s), %d organization(s).", len(names), len(orgs))
    return names, emails, orgs


def extract_info(text: str) -> tuple[list[str], list[str], list[str]]:
    """
    Main entry point for extracting PERSON, EMAIL, ORG using spaCy or GPT.
    """
    if use_gpt_extraction():
        logger.info("🧠 Using GPT for extraction.")
        try:
            result = extract_entities_with_gpt(text)
            if isinstance(result, dict):
                return (
                    result.get("person", []),
                    result.get("email", []),
                    result.get("organization", [])
                )
            else:
                logger.warning("⚠️ GPT result is not a dictionary. Got: %s", type(result))
        except Exception as e:
            logger.exception("❌ Error during GPT extraction.")
        return [], [], []
    else:
        return extract_info_spacy(text)
