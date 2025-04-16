import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Main project directory
PROJECT_DIR = Path(__file__).parent.parent.parent

INPUT_DIR = PROJECT_DIR / os.getenv("OUTPUT_FOLDER", "./output")
OUTPUT_DIR = PROJECT_DIR / os.getenv("PREPROCESSED_DIR", "./training/evaluation/preprocessed")

from pathlib import Path
import importlib.util
import pandas as pd

# Update this list to match your actual file paths
data_files = [
    "training/training_data.py",
    "training/name_data/synthetic_name_data.py",
    "training/name_data/paragraph_training_data.py"
]

def load_train_data(file_path):
    spec = importlib.util.spec_from_file_location("data_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TRAIN_DATA

# Compile TRAIN_DATA
all_train_data = []
for file_path in data_files:
    train_data = load_train_data(file_path)
    all_train_data.extend(train_data)

# Convert to DataFrame
records = []
for text, ann in all_train_data:
    for start, end, label in ann.get("entities", []):
        entity = text[start:end]
        records.append({
            "text": text,
            "entity": entity,
            "label": label
        })

df = pd.DataFrame(records)

# Save or preview
print(df.head())
df.to_csv("training_entity_breakdown.csv", index=False)



# if __name__ == "__main__":
#     process_all()
