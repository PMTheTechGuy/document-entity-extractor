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

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ENTITY_COLUMNS = {
    "Names": "PERSON",
    "Emails": "EMAIL",
    "Organizations": "ORG"
}

def preprocess_model_file(file_path):
    model_name = file_path.stem.replace("_extracted_data", "")
    df = pd.read_excel(file_path)

    rows = []
    for _, row in df.iterrows():
        for col, ent_type in ENTITY_COLUMNS.items():
            if pd.notna(row.get(col)):
                entities = [e.strip() for e in str(row[col]).split(",") if e.strip()]
                for entity in entities:
                    rows.append({
                        "Model": model_name,
                        "Entity Type": ent_type,
                        "Entity": entity,
                        "Predicted": 1,
                        "Actual": 0  # You will manually adjust this later
                    })

    return pd.DataFrame(rows)


def process_all():
    files = list(INPUT_DIR.glob("*model*_extracted_data.xlsx"))
    if not files:
        print("⚠️ No matching Excel files found.")
        return

    for file in files:
        print(f"📄 Processing: {file.name}")
        df = preprocess_model_file(file)
        output_file = OUTPUT_DIR / f"{file.stem}_preprocessed.csv"
        df.to_csv(output_file, index=False)
        print(f"✅ Saved: {output_file}")


if __name__ == "__main__":
    process_all()
