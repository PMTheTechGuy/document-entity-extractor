# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Merge and split multiple .spacy training files into train/dev sets
# Usage: Run this to create train.spacy and dev.spacy from multiple input files
# ──────────────────────────────────────────────────────────────────────────────

from spacy.tokens import DocBin
import spacy
from pathlib import Path
import random
from pathlib import Path

# def merge_spacy_files(input_paths, output_path):
#     merged = DocBin()
#     for path in input_paths:
#         print(f"📦 Merging {path}...")
#         doc_bin = DocBin().from_disk(path)
#         for doc in doc_bin.get_docs(spacy.blank("en").vocab):
#             merged.add(doc)
#     merged.to_disk(output_path)
#     print(f"✅ Merged {len(merged)} examples to {output_path}")
#
# if __name__ == "__main__":
#     input_files = [
#         Path("paragraph_training_data.spacy"),
#         Path("training_data.spacy"),
#     ]
#     output_file = Path("train_data.spacy")
#     merge_spacy_files(input_files, output_file)
#
#


def merge_and_split_spacy_files(input_paths, output_train, output_dev, split_ratio=0.8, seed=42):
    nlp = spacy.blank("en")
    all_docs = []

    for path in input_paths:
        print(f"📦 Merging {path}...")
        doc_bin = DocBin().from_disk(path)
        docs = list(doc_bin.get_docs(nlp.vocab))
        all_docs.extend(docs)

    print(f"📊 Total examples merged: {len(all_docs)}")

    # Shuffle and split
    random.seed(seed)
    random.shuffle(all_docs)
    split_index = int(len(all_docs) * split_ratio)
    train_docs = all_docs[:split_index]
    dev_docs = all_docs[split_index:]

    # Save both sets
    DocBin(docs=train_docs).to_disk(output_train)
    DocBin(docs=dev_docs).to_disk(output_dev)

    print(f"✅ Saved {len(train_docs)} to {output_train}")
    print(f"✅ Saved {len(dev_docs)} to {output_dev}")

if __name__ == "__main__":
    input_files = [
        Path("paragraph_training_data.spacy"),
        Path("raining_data.spacy"),
    ]
    merge_and_split_spacy_files(
        input_paths=input_files,
        output_train=Path("train.spacy"),
        output_dev=Path("dev.spacy")
    )
