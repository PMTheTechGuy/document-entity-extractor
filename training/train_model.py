# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Trains a custom Named Entity Recognition (NER) model using spaCy
#          and user-provided training data, then saves the model to disk.
# ──────────────────────────────────────────────────────────────────────────────

from training.name_data.training_data.synthetic_name_data import SYNTHETIC_TRAIN_DATA
import os
from dotenv import load_dotenv
import logging
from spacy.cli.train import train
from pathlib import Path

# Load enviroment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Ensure correct path is always passed
PROJECT_ROOT = Path(__file__).resolve().parent.parent
file_path = PROJECT_ROOT / os.getenv("LOG_DIR") / "train_model.log"

header = logging.FileHandler(file_path, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
header.setFormatter(formatter)
logger.addHandler(header)

# Combine traning data
# TRAIN_DATA = TRAIN_DATA_PARAGRAPH + SYNTHETIC_TRAIN_DATA + LABEL_STUDIO_TRAIN_DATA

# def train_custom_ner():
#     """
#         Trains a custom NER model using the 'en_core_web_sm'
#         spaCy pipeline and saves it to disk.
#     """
#     try:
#         # Load base model and access NER component
#         nlp = spacy.load("en_core_web_sm")
#         ner = nlp.get_pipe("ner")
#
#         # Add labels from training data to NER component
#         for _, annotations in TRAIN_DATA:
#             for ent in annotations["entities"]:
#                 ner.add_label(ent[2])
#
#         # Disable other pipes for training
#         other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
#         with nlp.disable_pipes(*other_pipes):
#             optimizer = nlp.resume_training()
#             for iteration in range(10):
#                 print(f"Training iteration {iteration + 1}")
#                 for text, annotations in TRAIN_DATA:
#                     doc = nlp.make_doc(text)
#                     example = Example.from_dict(doc, annotations)
#                     nlp.update([example], drop=0.3, sgd=optimizer)
#         # Save the model to disk
#         model_dir = "custom_ner_person_model"
#         os.makedirs(model_dir, exist_ok=True)
#         nlp.to_disk(model_dir)
#         logger.info(f"✅ Custom NER model saved to: {model_dir}/")
#
#     except Exception as e:
#         logger.error(f"Error during model training: {e}", exc_info=True)

def run_cli_training():
    config_path = Path("config.cfg")  # Adjust if your config is elsewhere
    output_path = Path("custom_ner_person_model")

    if not config_path.exists():
        raise FileNotFoundError("❌ config.cfg not found. Generate it using 'spacy init config'.")

    train(
        config_path=config_path,
        output_path=output_path,
        overrides={
            "paths.train": "spacy_data/train_data.spacy",
            "paths.dev": "spacy_data/dev.spacy",
        }
    )

if __name__ == "__main__":
    # train_custom_ner()
    run_cli_training()
