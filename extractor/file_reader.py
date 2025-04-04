# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Provides utility functions to extract text from PDF, DOCX, and TXT files.
# ──────────────────────────────────────────────────────────────────────────────

import pdfplumber
import docx
import logging

# Setup logging
logger = logging.getLogger(__name__)

def read_pdf(file_path):
    """Extracts text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
        logger.info(f"Successfully read PDF file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to read PDF file: {file_path}: {e}")
    return text

def read_docx(file_path):
    """Extracts text from a DOCX file using python-docx."""
    try:
        doc = docx.Document(file_path)
        logger.info(f"Successfully read DOCX file: {file_path}")
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Failed to read DOCX file: {file_path}: {e}")
        return ""

def read_txt(file_path):
    """Reads plain text from a TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            logger.info(f"Successfully read plain text file: {file_path}")
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read plain text file: {file_path}: {e}")
        return ""

def read_file(file_path):
    """Determines file type and extracts text accordingly."""
    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.endswith(".docx"):
        return read_docx(file_path)
    elif file_path.endswith(".txt"):
        return read_txt(file_path)
    else:
        logger.error(f"Failed to determine file type: {file_path}.")
        return ""

