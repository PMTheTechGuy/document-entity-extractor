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
from dotenv import load_dotenv
from pathlib import Path
from utils.logger import logger
import os

# Load environment variables
load_dotenv()

# Ensure correct path is always passed
PROJECT_ROOT = Path(__file__).resolve().parent

# Define input/output folder paths from environment variables
INPUT_FOLDER = os.path.join(PROJECT_ROOT, os.getenv("INPUT_FOLDER"))
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, os.getenv("OUTPUT_FOLDER"))
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "custom_person_model_extracted_data.xlsx")

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
            names, emails, orgs = extract_info(text)

            # print("👤 Names:", names)
            # print("📧 Emails:", emails)
            # print("🏢 Orgs:", orgs)

            # Store result in dictionary
            results.append({
                "Filename": os.path.basename(file),
                "Names": ", ".join(set(names)),
                "Emails": ", ".join(set(emails)),
                "Organizations": ", ".join(set(orgs))
            })
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")

    # Export extracted data to Excel
    export_to_excel(results, OUTPUT_FILE)
    logger.info(f"✅ Extraction complete. Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
