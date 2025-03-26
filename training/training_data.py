# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Contains manually annotated training data for use in training a
#           custom spaCy Named Entity Recognition (NER) model.
# ──────────────────────────────────────────────────────────────────────────────

# Format: Each tuple contains a text sample and a dictionary with entity annotations.
# Entity format: (start_char_index, end_char_index, entity_label)

# Training data for custom module
TRAIN_DATA = [
    (
        "John W. Smith worked at The Wesley Center and studied at the University of Arkansas.",
        {"entities": [(0, 13, "PERSON"), (24, 41, "ORG"), (61, 83, "ORG")]}
    ),
    (
        "IM A. Sample is a member of the American Business Women's Association.",
        {"entities": [(0, 12, "PERSON"), (32, 69, "ORG")]}
    ),
    (
        "Resume by Peter Holtmann from ESA and Ariane Group.",
        {"entities": [(10, 24, "PERSON"), (30, 33, "ORG"), (38, 50, "ORG")]}
    ),
    (
        "Jane Doe attended Bellevue University.",
        {"entities": [(0, 8, "PERSON"), (18, 37, "ORG")]}
    ),
    (
        "Samantha Lee interned at NASA and graduated from MIT.",
         {"entities": [(0, 12, "PERSON"), (25, 29, "ORG"), (49, 52, "ORG")]}
    ),
    (
        "Peter Holtmann collaborated with ESA and Ariane Group.",
        {"entities": [(0, 14, "PERSON"), (33, 36, "ORG"), (41, 53, "ORG")]}
    )

]