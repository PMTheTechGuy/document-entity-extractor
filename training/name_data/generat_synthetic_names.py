# Author: Paul-Michael Smith
# Purpose: Generate synthetic training data using SSA baby names
# Output: training/synthetic_name_data.py containing spaCy formatted examples

import os
import random
from pathlib import Path
from logging import getLogger
import sqlite3

# Initialize logger
logger = getLogger(__name__)

# Config
NAME_DIR = Path("names")
OUTPUT_DIR = Path("training/synthetic_name_data.py")
SURNAME_DB = Path("clean_names/clean_surname.db")

# Template that stores the structure for training the model
SENTENCE_TEMPLATES = [
    "My name is {name}.",
    "{name} attended the meeting.",
    "{name} signed the contract.",
    "{name} is our new manager.",
    "We had lunch with {name} yesterday.",
    "Have you seen {name} today?",
    "{name} will join us shortly.",
    "The client spoke with {name}.",
    "{name} is leading the project.",
    "Everyone was impressed by {name}."
    "{name} signed the agreement yesterday.",
    "The keynote speaker was {name}.",
    "Please contact {name} regarding the invoice.",
    "{name} has submitted the final report.",
    "We received feedback from {name}.",
    "The interview with {name} was insightful.",
    "{name} is leading the research team.",
    "The manager introduced {name} to the board.",
    "For further clarification, reach out to {name}.",
    "{name} will represent the company at the event."
]

# Extended sentence templates for name insertion
short_to_mid_templates = [
    "My name is {name}.",
    "{name} attended the meeting.",
    "{name} signed the contract.",
    "{name} is our new manager.",
    "We had lunch with {name} yesterday.",
    "Have you seen {name} today?",
    "{name} will join us shortly.",
    "The client spoke with {name}.",
    "{name} is leading the project.",
    "Everyone was impressed by {name}.",
    "{name} signed the agreement yesterday.",
    "The keynote speaker was {name}.",
    "Please contact {name} regarding the invoice.",
    "{name} has submitted the final report.",
    "We received feedback from {name}.",
    "The interview with {name} was insightful.",
    "{name} is leading the research team.",
    "The manager introduced {name} to the board.",
    "For further clarification, reach out to {name}.",
    "{name} will represent the company at the event.",
    "{name} submitted the proposal just in time for the deadline.",
    "The board appreciated {name}'s contributions during the presentation.",
    "We need to follow up with {name} about the pending documents.",
    "Please have {name} review the revised policy before noon.",
    "{name} just emailed the latest figures to the finance team.",
    "Everyone was surprised by {name}'s insightful analysis.",
    "The award was presented to {name} at the ceremony.",
    "{name} has taken the lead on the new initiative.",
    "We'll need a signature from {name} by Friday.",
    "Marketing has already spoken to {name} about the rollout."
]

long_templates = [
    "During the quarterly meeting, {name} outlined a comprehensive strategy that impressed both clients and executives alike.",
    "Despite the challenges faced by the department, {name} managed to deliver outstanding results ahead of schedule.",
    "According to internal sources, {name} will be heading the negotiations with the international partners.",
    "After much deliberation, the committee decided that {name} was the best candidate for the position.",
    "It was {name} who first raised concerns about the data inconsistencies that were later confirmed.",
    "The presentation given by {name} offered a refreshing perspective on the company's long-term goals.",
    "We were all surprised when {name} volunteered to coordinate the entire event on such short notice.",
    "Following the press release, {name} responded to several inquiries from industry reporters.",
    "The feedback received from stakeholders highlighted {name}'s clear communication and leadership.",
    "Before moving forward, we need to ensure that {name} has approved the final draft.",
    "I remember {name} mentioned this idea during last month’s brainstorming session.",
    "Wasn’t {name} the one who handled the supplier negotiations last time?",
    "{name} might have more insight into that issue, let’s loop them in.",
    "That sounds like something {name} would be interested in managing.",
    "When {name} spoke at the conference, the room went completely silent.",
    "We’ve already looped in {name} to coordinate the logistics.",
    "I believe {name} has the experience needed to guide the project through phase two.",
    "Let’s assign this task to {name} since they’ve handled similar cases before.",
    "{name} was recognized for their outstanding contributions in last year’s awards ceremony.",
    "If there’s anyone who can handle this under pressure, it’s {name}."
]

# Combine all templates
all_templates = short_to_mid_templates + long_templates

def load_first_names(directory: Path) -> list[str]:
    """
    Load unique names from all SSA name files.
    """
    names = []
    for file in directory.glob("yob*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 1:
                    name = parts[0].strip()
                    if name and name.isalpha():
                        names.append(name)
    logger.info(f" Loaded {len(names)} unique first names from {directory}.")
    return list(set(names))

def load_last_names(db_path: Path) -> list[str]:
    """
        Load surnames from SQLite database.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT surname FROM surname ORDER BY surname ASC")
        surnames = [row[0].capitalize() for row in cursor.fetchall()]
    logger.info(f" Loaded {len(surnames)} unique surnames from SQLite database.")
    return surnames

def generate_training_data(first_names, last_names, templates, limit=100000) -> list:
    """Generate spaCy training data."""
    examples = []
    for _ in range(limit):
        first = random.choice(first_names)
        last = random.choice(last_names)
        full_name = f"{first} {last}"
        template = random.choice(templates)
        sentence = template.format(name=full_name)
        start = sentence.index(full_name)
        end = start + len(full_name)
        examples.append((sentence, {"entities": [(start, end, "PERSON")]}))
    logger.info(f"Generated {len(examples)} synthetic training examples.")
    return examples

# def generate_training_data(names, templates, limit=500):
#     """
#         Generate spaCy-compatible training data from name list and templates.
#     """
#
#     example = []
#     sample_name = random.sample(names, min(limit, len(names)))
#     for name in sample_name:
#         template = random.choice(templates)
#         sentence = template.format(name=name)
#         start = sentence.index(name)
#         end = start + len(name)
#         example.append((sentence, {"entities": [(start, end, "PERSON")]}))
#     logger.info(f" Generated {len(example)} synthetic training examples.")
#     return example

def save_training_data(examples, path):
    """Save training examples to Python file in spaCy format."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Auto-generated synthetic training data for PERSON labels\n")
        f.write("SYNTHETIC_TRAIN_DATA = [\n")
        for text, ann in examples:
            escaped = text.replace("\"", "\\\"")
            f.write(f'    ("{escaped}", {{"entities": {ann["entities"]}}}),\n')
        f.write("]\n")
    logger.info(f"💾 Saved training data to: {path}")

if __name__ == "__main__":
    first_names = load_first_names(NAME_DIR)
    last_names = load_last_names(SURNAME_DB)
    print(f"✅ First names: {len(first_names)}, Last names: {len(last_names)}")
    synthetic_examples = generate_training_data(first_names, last_names, all_templates, limit=100000)
    save_training_data(synthetic_examples, OUTPUT_DIR)
    print("✅ Synthetic name data generation completed.")



    # all_names = load_names(NAME_DIR)
    # print(f"Total names: {len(all_names)}")
    # synthetic_examples = generate_training_data(all_names, all_templates, limit=500)
    # save_training_data(synthetic_examples, OUTPUT_DIR)
    # print("Synthetic name data generation completed.")