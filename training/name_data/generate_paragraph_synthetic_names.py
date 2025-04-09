# generate_paragraph_synthetic_names.py

import random
import sqlite3
import spacy
from pathlib import Path
import re
from generat_synthetic_names import load_first_names
from dotenv import load_dotenv
import os


load_dotenv()

nlp = spacy.blank("en")

DB_PATH = Path(os.getenv("DB_PATH"))
NAME_DIR = Path(os.getenv("NAME_DIR"))


# Load names from SQLite DB
def load_names():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT Surname FROM surname ORDER BY RANDOM() LIMIT 300")
    last_names = [row[0] for row in cursor.fetchall()]
    first_names = load_first_names(NAME_DIR)  # You can expand this
    return first_names, last_names

# Paragraph templates
TEMPLATES = [
    "Today, {names} met at the annual leadership summit to discuss innovation and collaboration.",
    "{names} were among the experts quoted in the recent article on emerging technologies.",
    "A heated debate broke out between {names} during the policy roundtable.",
    "The winners of this year's humanitarian award include {names}.",
    "In the new book, the main characters are {names}, all of whom bring unique perspectives.",
]

def generate_examples():
    examples = []
    first_names, last_names = load_names()

    for _ in range(50):
        num_people = random.randint(2, 5)
        chosen_names = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(num_people)]
        name_text = ", ".join(chosen_names[:-1]) + f", and {chosen_names[-1]}" if len(chosen_names) > 2 else " and ".join(chosen_names)

        template = random.choice(TEMPLATES)
        paragraph = template.format(names=name_text)
        doc = nlp.make_doc(paragraph)

        entities = []
        for name in chosen_names:
            start = paragraph.find(name)
            end = start + len(name)
            if start != -1:
                entities.append((start, end, "PERSON"))

        examples.append((paragraph, {"entities": entities}))

    return examples

def save_examples_to_file(examples, path="training/paragraph_training_data.py"):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Auto-generated paragraph-style PERSON entity examples\n")
        f.write("TRAIN_DATA_PARAGRAPH = [\n")
        for text, ann in examples:
            escaped_text = text.replace('"', '\\"')
            f.write(f'    ("{escaped_text}", {{\'entities\': {ann["entities"]}}}),\n')
        f.write("]\n")
    print(f"✅ Saved {len(examples)} paragraph examples to {path}")

if __name__ == "__main__":
    data = generate_examples()
    save_examples_to_file(data)