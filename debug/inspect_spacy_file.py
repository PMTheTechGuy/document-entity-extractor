import spacy
from spacy.tokens import DocBin

# Load your binary training data
doc_bin = DocBin().from_disk("../training/training_data.spacy")
docs = list(doc_bin.get_docs(spacy.blank("en").vocab))

for i, doc in enumerate(docs):
    print(f"\nExample {i+1}:")
    print(doc.text)
    print([(ent.text, ent.label_) for ent in doc.ents])
