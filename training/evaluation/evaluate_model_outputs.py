"""
Author: PM The Tech Guy
Created: 2025-03-25
Purpose: Main execution script for extracting names, emails, and organizations
         from input files and saving the results to an Excel file.
"""


# training/evaluation/evaluate_model_outputs.py

import os
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent # Project root for this file
OUTPUT_FOLDER = PROJECT_ROOT / os.getenv("OUTPUT_FOLDER", "./output")

EVAL_OUTPUT_CSV = os.path.join(OUTPUT_FOLDER, "Model_Evaluation_Scores.csv")

def evaluate_model_output(df):
    results = []
    for entity in df["Entity Type"].unique():
        subset = df[df["Entity Type"] == entity]
        precision, recall, f1, _ = precision_recall_fscore_support(
            subset["Actual"], subset["Predicted"], average="binary", pos_label=1, zero_division=0
        )
        results.append({
            "Model": df["Model"].iloc[0],
            "Entity Type": entity,
            "Precision": round(precision, 3),
            "Recall": round(recall, 3),
            "F1 Score": round(f1, 3)
        })
    return results

def load_and_evaluate_all():
    all_scores = []

    for filename in os.listdir(OUTPUT_FOLDER):
        if "model" in filename.lower() and filename.endswith(".xlsx"):
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            print(f"📄 Evaluating: {filename}")

            try:
                df = pd.read_excel(filepath)
                if {"Model", "Entity Type", "Actual", "Predicted"}.issubset(df.columns):
                    all_scores.extend(evaluate_model_output(df))
                else:
                    print(f"⚠️ Missing required columns in: {filename}")
            except Exception as e:
                print(f"❌ Failed to read {filename}: {e}")

    if all_scores:
        score_df = pd.DataFrame(all_scores)
        score_df.to_csv(EVAL_OUTPUT_CSV, index=False)
        print(f"\n✅ Evaluation complete. Results saved to: {EVAL_OUTPUT_CSV}")
        print(score_df)
    else:
        print("⚠️ No valid model files found or evaluated.")

if __name__ == "__main__":
    load_and_evaluate_all()
