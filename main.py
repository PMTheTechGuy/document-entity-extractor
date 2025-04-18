"""
Author: PM The Tech Guy
Created: 2025-03-25
Purpose: Main execution script for extracting names, emails, and organizations
         from input files and saving the results to an Excel file.
"""

from extractor.file_reader import read_file
from extractor.text_extractor import extract_info
from utils.file_handler import get_all_files
from utils.export_excel import export_to_excel
from datetime import datetime
from utils.config import use_gpt_extraction
from dotenv import load_dotenv
from pathlib import Path
from utils.logger import logger
import os

# Load environment variables
load_dotenv()

# Determine model label
if use_gpt_extraction():
    model_tag = "gpt"
else:
    try:
        from extractor.text_extractor import nlp
        model_tag = "custom" if "custom_ner" in str(nlp.meta.get("name", "")) else "default"
    except Exception:
        model_tag = "default"

# Add timestamp for versioning
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"{model_tag}_extracted_data_{timestamp}.xlsx"

# Ensure correct path is always passed
PROJECT_ROOT = Path(__file__).resolve().parent

# Define input/output folder paths from environment variables
INPUT_FOLDER = os.path.join(PROJECT_ROOT, os.getenv("INPUT_FOLDER"))
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, os.getenv("OUTPUT_FOLDER"))
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, output_filename)

def main():
    logger.info(f"Scanning folder: {INPUT_FOLDER}")

    # Get list of all files in the input directory
    files = get_all_files(INPUT_FOLDER)
    results = []

    for file in files:
        logger.info(f"Processing {file}...")
        try:
            # Read file content
            text = read_file(file)
            # print("📃 Preview of extracted text:")
            # print(text[:300])  # First 300 characters

            # Extract information using NLP pipeline
            # names, emails, orgs = extract_info(text)

            # Extract structured results from spaCy or GPT
            result = extract_info(text)

            # Ensure result is a dictionary
            if not isinstance(result, dict):
                logger.warning("⚠️ Unexpected format returned from extract_info. Skipping.")
                continue

            names = result.get("person", [])
            emails = result.get("email", [])
            orgs = result.get("organization", [])
            confidences_raw = result.get("confidence_scores", [])
            file_extension = os.path.splitext(file)[1].lower()  # e.g., ".pdf", ".docx"

            # Group confidence scores by entity type
            confidence_lookup = {"PERSON": [], "ORG": [], "EMAIL": []}
            for item in confidences_raw:
                if isinstance(item, dict):
                    label = item.get("label")
                    score = item.get("confidence")
                    if label in confidence_lookup and isinstance(score, (float, int)):
                        confidence_lookup[label].append(score)
                else:
                    logger.warning(f"⚠️ Skipping malformed confidence entry: {item}")

            # Build result row
            results.append({
                "Filename": os.path.basename(file),
                "Source Type": file_extension,
                "Names": ", ".join(set(names)),
                "Name Confidences": ", ".join([f"{c:.2f}" for c in confidence_lookup["PERSON"]]),
                "Emails": ", ".join(set(emails)),
                "Email Confidences": ", ".join([f"{c:.2f}" for c in confidence_lookup["EMAIL"]]),
                "Organizations": ", ".join(set(orgs)),
                "Org Confidences": ", ".join([f"{c:.2f}" for c in confidence_lookup["ORG"]]),
                "Model Source": result.get("source", "unknown"),
            })

            # file_extension = os.path.splitext(file)[1].lower() # e.g., ".pdf", ".docx", ".txt"

            # print("👤 Names:", names)
            # print("📧 Emails:", emails)
            # print("🏢 Orgs:", orgs)

            # # Store result in dictionary
            # results.append({
            #     "Filename": os.path.basename(file),
            #     "Source Type": file_extension,
            #     "Names": ", ".join(set(names)),
            #     "Emails": ", ".join(set(emails)),
            #     "Organizations": ", ".join(set(orgs))
            # })
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")

    # Export extracted data to Excel
    export_to_excel(results, OUTPUT_FILE)
    logger.info(f"✅ Extraction complete. Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
