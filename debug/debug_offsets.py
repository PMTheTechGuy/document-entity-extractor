import spacy
from training.training_data import TRAIN_DATA

nlp = spacy.blank("en")

def show_token_boundaries(text):
    print(f"\n🔍 Inspecting: {text}\n")
    doc = nlp(text)
    for token in doc:
        print(f"{token.text:<15} start={token.idx:<3} end={token.idx + len(token.text)}")

# Example text to inspect
# show_token_boundaries("Samantha Lee interned at NASA and graduated from MIT.")
# show_token_boundaries("Peter Holtmann collaborated with ESA and Ariane Group.")

for userStr, ent in TRAIN_DATA:
    show_token_boundaries(userStr)