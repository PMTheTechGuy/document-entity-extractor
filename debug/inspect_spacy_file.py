import spacy
import os
from spacy.tokens import DocBin

# Ensure correct path is always passed
base_dir = os.path.dirname(os.path.dirname(__file__)) # go up from debug/ to root
file_path = os.path.join(base_dir, "training", "training_dataset/train_data.spacy")

# Load your binary training data
doc_bin = DocBin().from_disk(file_path)
docs = list(doc_bin.get_docs(spacy.blank("en").vocab))

for i, doc in enumerate(docs):
    print(f"\nExample {i+1}:")
    print(doc.text)
    print([(ent.text, ent.label_) for ent in doc.ents])
