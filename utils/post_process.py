# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Post-process extracted entities to remove noise and improve clarity
# ──────────────────────────────────────────────────────────────────────────────

import re
import os
import logging
from pathlib import Path
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the logs directory if it doesn't exist
# Ensure correct path is always passed
PROJECT_ROOT = Path(__file__).resolve().parent.parent
log_dir = PROJECT_ROOT / os.getenv("LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)

# Setup logging configuration
log_file_path = os.path.join(log_dir, "post_process.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)
logger.info("✅ Post-processing logger setup complete.")


# Example list of some valid acronyms (can expand this later)
VALID_ACRONYMS = {
    "NASA", "MIT", "IBM", "UN", "WHO", "FBI", "CIA", "NSA",
    "FDA", "EPA", "IRS", "SEC", "ATF", "CDC", "NIH"
}

# Common filler or noise words to exclude from entities
NOISE_WORDS = {"and", "or", "of", "the", "in", "on", "to", "with", "a", "an", "BA", "AS", "•", "GPA", "Scale", " - "}


def is_valid_acronym(word):
    """Check if a word is a valid acronym based on the known list or pattern."""
    return word in VALID_ACRONYMS or (word.issupper() and 2 < len(word) <= 5)

def normalize_entity(entity):
    """Clean up entity string by removing noise and formatting issues."""
    entity = entity.strip()
    entity = re.sub(r"[\.,;:]+$", "", entity) # trailing punctuation
    entity = re.sub(r"\s+", " ", entity) # extra spaces
    return entity

def clean_entities(entities, entity_type="ORG"):
    """
    Applies cleaning functions to entities.
    Clean and filter extracted entity list.
    """
    cleaned = set()
    for ent in entities:
        norm = normalize_entity(ent)
        # Remove if it's mostly special characters or digits
        if not re.search(r'[A-Za-z]', norm) or re.match(r'^[\W\d\s]+$', norm):
            continue

        # Remove if it's one short word or a known noise word
        if len(norm.split()) == 1 and norm.lower() in NOISE_WORDS:
            continue

        # Basic filter: remove suspiciously short or long items
        if len(norm) < 3 or len(norm) > 100:
            continue

        cleaned.add(norm)
    return list(cleaned)

    # for org in entities:
    #     if not isinstance(org, str):
    #         continue # skip if it's not a string
    #
    #     org = org.strip(",.-:\n")
    #
    #     # Keep acronyms like NSA, avoid full sentences
    #     if org.isupper() and 2 <= len(org) <= 6:
    #         cleaned.add(org)
    #         continue
    #
    #     # Skp overly long orgs or malformed strings
    #     if len(org.split()) > 10:
    #         continue
    #
    #     cleaned.add(org)
    # return list(cleaned)

    # for ent in entities:
    #     norm = normalize_entity(ent)
    #     if entity_type == "ORG":
    #         if len(norm) < 2:
    #             print(entity_type)
    #             continue
    #         if norm.isupper() and not is_valid_acronym(norm):
    #             print(entity_type)
    #             continue
    #     cleaned.append(norm)
    # return list(cleaned)







