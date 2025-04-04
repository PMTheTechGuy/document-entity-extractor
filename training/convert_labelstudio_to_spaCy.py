# ────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Convert Label Studio JSON export to spaCy training data testing.
# Usage: Run this script to generate training_data.py with TRAIN_DATA
# ────────────────────────────────────────────────────────────────

import json
from pathlib import Path
import os

# Ensure correct path is always passed
base_dir = os.path.dirname(os.path.dirname(__file__)) # go up from debug/ to root
input_file_path = os.path.join(base_dir, "label_studio", "data", "export", "project-1-at-2025-03-31-20-48-a664c004.json")
output_file_path = os.path.join(base_dir, "training", "training_data.py")

# Paths
output_path = Path(output_file_path)
input_path = Path(input_file_path)


# Load the JSON file
try:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    print(f"✅ File opened: {input_file_path}\n")
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"❌ Error loading JSON: {e}")
    exit(1)

train_data = []

for item in data:
    text = item["data"]["text"]
    entities = []

    for result in item.get("annotations", [])[0].get("result", []):
        if result["type"] == "labels":
            start = result["value"]["start"]
            end = result["value"]["end"]
            label = result["value"]["labels"][0]
            entities.append((start, end, label))

    train_data.append((text, {"entities": entities}))

# Write to training_data.py
output_path.parent.mkdir(parents=True, exist_ok=True)
try:
    # Convert each data point to a spaCy-style entry
    formatted_data = []
    for text, ann in train_data:
        escaped_text = text.replace("\"", "\\\"").replace("\n", "\\n")
        formatted_data.append(f"    (\"{escaped_text}\", {{'entities': {ann['entities']}}}),\n")

    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Remove the last line if it contains only the closing bracket
        if lines and lines[-1].strip() == "]":
            lines = lines[:-1]  # drop the last line

        lines.extend(formatted_data)
        lines.append("]\n") # Re-add the closing bracket

        # Write everything back to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Auto-generated spaCy training data from Label Studio\n")
            f.write("TRAIN_DATA = [\n")
            f.writelines(formatted_data)
            f.write("\n]\n")

    print(f"✅ Successfully converted {len(train_data)} examples to spaCy format.")
except Exception as e:
    print(f"Issue: {e}")

