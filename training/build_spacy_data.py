# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Converts annotated training examples into a .spacy binary format
#           compatible with spaCy model training.
# ──────────────────────────────────────────────────────────────────────────────

import spacy
from spacy.tokens import DocBin
from training.training_data import TRAIN_DATA
import logging
import os

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("../logs/train.log", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def build_spacy_docbin(output_path="../training/training_data.spacy"):
    """
        Converts the training data into spaCy's DocBin format for
        efficient model training.

        Args:
            output_path (str): Path where the .spacy file will be saved.
    """
    logger.info("Starting to build spaCy DocBin (.spacy file) for training data")

    # Start with blank English pipeline
    nlp = spacy.blank("en")
    doc_bin = DocBin()

    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []

        for start, end, label in annotations["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                logger.warning(f"⚠️ Skipping misaligned span: '{text[start:end]}' in: '{text}'")
            else:
                ents.append(span)

        doc.ents = ents
        doc_bin.add(doc)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc_bin.to_disk(output_path)
    logger.info(f"✅ Saved aligned training data to {output_path}")


if __name__ == "__main__":
    build_spacy_docbin()
