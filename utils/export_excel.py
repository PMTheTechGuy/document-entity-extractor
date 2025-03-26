# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Exports extracted entity data to an Excel file for downstream use or delivery.
# ──────────────────────────────────────────────────────────────────────────────

import pandas as pd
import os
import logging

# Logging setup
logger = logging.getLogger(__name__)

# Exports the results to a directory
def export_to_excel(results, output_path):
    """
    Exports the given results to an Excel file.

    Args:
        results (list): A list of dictionaries containing extracted data.
        output_path (str): Full path to the Excel file to write.
    """
    try:
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(results)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write DataFrame to Excel
        df.to_excel(output_path, index=False)
        logger.info(f"Exported extracted data to Excel file at: {output_path} successfully.")
    except Exception as e:
        logger.error(f"Failed to export extracted data to Excel file at {output_path}: {e}", exc_info=True)