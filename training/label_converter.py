# ────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Convert all Label Studio JSON exports in the input folder
#          to spaCy training format and append to training_data.py
# ────────────────────────────────────────────────────────────────

import json
import shutil
import os
from pathlib import Path
import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Ensure correct path is always passed
base_dir = os.path.dirname(os.path.dirname(__file__)) # go up from traning/ to root
file_path = os.path.join(base_dir, "logs", "train_model.log")

header = logging.FileHandler(file_path, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
header.setFormatter(formatter)
logger.addHandler(header)

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "label_studio" / "data" / "export"
ARCHIVE_DIR = INPUT_DIR / "archive"
OUTPUT_PATH = BASE_DIR / "training" / "training_data.py"

ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def convert_json_to_spacy_format(input_path):
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"📂 Processing file: {input_path.name}")
        if not isinstance(data, list):
            logger.error(f"❌ Unexpected JSON structure in file {input_path.name}. Expected a list of annotations.")
            return []
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"❌ Failed to load {input_path.name}: {e}")
        return []

    converted = []
    for item in data:
        text = item.get("data", {}).get("text", "")
        entities = []

        for result in item.get("annotations", [])[0].get("result", []):
            if result.get("type") == "labels":
                start = result["value"]["start"]
                end = result["value"]["end"]
                label = result["value"]["labels"][0]
                entities.append((start, end, label))

        escaped_text = text.replace('"', '\\"').replace("\n", "\\n")
        converted.append(f'    ("{escaped_text}", {{"entities": {entities}}}),\n')

    return converted

def append_to_training_file(entries):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Remove the trailing closing bracket if present
        if lines and lines[-1].strip() == "]":
            lines.pop()

        lines.extend(entries)
        lines.append("]\n")

        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)
    else:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write("# Auto-generated spaCy training data from Label Studio\n")
            f.write("TRAIN_DATA = [\n")
            f.writelines(entries)
            f.write("]\n")

    logger.info(f"✅ Added {len(entries)} entries to {OUTPUT_PATH.name}.")


def process_all_json():
    all_files = list(INPUT_DIR.glob("*.json"))

    if not all_files:
        logger.warning("🚫 No new files found in the input folder.")
        return

    total = 0
    for json_file in all_files:
        entries = convert_json_to_spacy_format(json_file)
        if entries:
            append_to_training_file(entries)
            shutil.move(str(json_file), ARCHIVE_DIR / json_file.name)
            logger.info(f"📦 Archived: {json_file.name}")
            total += len(entries)

    logger.info(f"🎯 Completed conversion. Total new entries: {total}")


if __name__ == "__main__":
    process_all_json()
