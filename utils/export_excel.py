# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Exports extracted entity data to an Excel file for downstream use or delivery.
# ──────────────────────────────────────────────────────────────────────────────
from pathlib import Path

import pandas as pd
import os
import logging

# Logging setup
logger = logging.getLogger(__name__)


# Exports the results to a directory
def export_to_file(results, output_path: str, format='xlsx'):
    """
    Exports the given results to an Excel file.

    Args:
        results (list): A list of dictionaries containing extracted data.
        output_path (str): Full path to the Excel file to write.
    """
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(results)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_path = Path(output_path)
    print("💡 Exporting format:", format, "| File path:", output_path)

    try:
        if format == 'xlsx':
            # Write DataFrame to Excel
            df.to_excel(output_path, index=False)
            logger.info(f"Exported the extracted data to Excel file at: {output_path} successfully.")
        elif format == 'csv':
            df.to_csv(output_path, index=False)
            logger.info(f"Exported the extracted data to CSV file at: {output_path} successfully.")
        else:
            raise ValueError(f"Unsupported export format.")
    except Exception as e:
        logger.error(f"Failed to export the extracted data to the Excel file at {output_path}: {e}", exc_info=True)
