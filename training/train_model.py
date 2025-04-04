# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Trains a custom Named Entity Recognition (NER) model using spaCy
#          and user-provided training data, then saves the model to disk.
# ──────────────────────────────────────────────────────────────────────────────

import spacy
from spacy.training.example import Example
from training_data import TRAIN_DATA
import os
import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Ensure correct path is always passed
base_dir = os.path.dirname(os.path.dirname(__file__)) # go up from traning/ to root
file_path = os.path.join(base_dir, "logs", "train_model.log")

header = logging.FileHandler(file_path, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
header.setFormatter(formatter)
logger.addHandler(header)


def train_custom_ner():
    """
        Trains a custom NER model using the 'en_core_web_sm'
        spaCy pipeline and saves it to disk.
    """
    try:
        # Load base model and access NER component
        nlp = spacy.load("en_core_web_sm")
        ner = nlp.get_pipe("ner")

        # Add labels from training data to NER component
        for _, annotations in TRAIN_DATA:
            for ent in annotations["entities"]:
                ner.add_label(ent[2])

        # Disable other pipes for training
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):
            optimizer = nlp.resume_training()
            for iteration in range(10):
                print(f"Training iteration {iteration + 1}")
                for text, annotations in TRAIN_DATA:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    nlp.update([example], drop=0.3, sgd=optimizer)
        # Save the model to disk
        model_dir = "custom_ner_model"
        os.makedirs(model_dir, exist_ok=True)
        nlp.to_disk(model_dir)
        logger.info(f"✅ Custom NER model saved to: {model_dir}/")

    except Exception as e:
        logger.error(f"Error during model training: {e}", exc_info=True)

if __name__ == "__main__":
    train_custom_ner()
