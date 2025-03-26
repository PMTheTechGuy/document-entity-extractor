# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Scans directories recursively and returns a list of supported files (.pdf, .docx, .txt).
# ──────────────────────────────────────────────────────────────────────────────

import os
import logging


# Setup logging
logger = logging.getLogger(__name__)

def get_all_files(folder, extensions=None):
    """
        Scans the specified folder and subfolders for files matching given extensions.

    Args:
        folder (str): Path to the folder to scan.
        extensions (list, optional): List of file extensions to include. Defaults to PDF, DOCX, and TXT.

    Returns:
        list: Full file paths of matching files.
    """
    if extensions is None:
        extensions = [".pdf", ".docx", ".txt"]
        logger.info(f"No extensions provided. Using default extensions: {', '.join(extensions)}")

    all_files = []
    try:
        for root, _, files in os.walk(folder):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    all_files.append(os.path.join(root, file))
        logger.info(f"Found {len(all_files)} files in folder: {folder}.")
    except FileNotFoundError as e:
        logger.error(f"Folder could not be found: {folder}", e, exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error occurred while scanning folder: {folder}",e , exc_info=True)

    return all_files
