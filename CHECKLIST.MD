# 📌 AI File Extraction Tool – Project Roadmap

## ✅ Phase 1: Finalize MVP (`v1`) – Clean & Reliable

### 🔧 Project Cleanup
- [x] Review and rename folders for clarity (`/training`, `/extractor`, `/debug`, etc.)
- [x] Archive legacy/testing scripts to `/debug` or `/archive`
- [X] Standardize file structure (input/output directories in `.env`)

### 📁 Model & Data
- [X] Save `custom_ner_person_model` as versioned snapshot (`v1`)
- [X] Back up `config.cfg` and key training scripts used
- [X] Store training datasets (`.spacy`) clearly labeled

### 📝 README & Documentation
- [ ] Add clear instructions for:
  - [ ] Uploading documents
  - [ ] Annotating with Label Studio
  - [ ] Converting annotations to training data
  - [ ] Running training and exporting Excel results
- [ ] Include example screenshots of Excel output
- [ ] Add system requirements and setup guide

### 📤 GitHub Polish
- [X] Clean up `.gitignore` for unnecessary system files
- [ ] Add `LICENSE`, `CONTRIBUTING.md` (optional)
- [ ] Write a clear project description + usage section

---

## 🚀 Phase 2: Build Foundation for Smarter AI Tool (SaaS Ready)

### 🧩 Modular Design
- [ ] Turn each task into reusable functions/modules:
  - [ ] Annotation Converter
  - [ ] Data Splitter (train/dev)
  - [ ] Model Trainer
  - [ ] Post-processing

### 🤖 Data + Training Improvements
- [ ] Expand synthetic training with full name + paragraph context
- [ ] Create `org`-focused training datasets next
- [ ] Add confidence thresholds to post-processing output
- [ ] Add acronym linking & smart organization merging

### 📊 Evaluation + Version Tracking
- [ ] Track metrics (precision, recall, F1) per model version
- [ ] Save training logs to file
- [ ] Store training dataset size, iteration count, and timestamp

### 💡 Future SaaS Prep
- [ ] Plan upload pipeline for end-users (raw doc → suggested labels → confirm/edit)
- [ ] Add queue logic for retraining when X new documents are annotated
- [ ] Draft UI layout if converting to web app later

---

## 🗂 Suggested Folder Structure

```bash
AIDataExtractionTool/
├── extractor/           # Extraction logic & spaCy usage
├── training/            # Training data, scripts, config files
│   ├── name_data/       # Surname + synthetic generation
│   └── org_data/        # (Future) organization-related data
├── label_studio/        # Annotation exports + converter
├── debug/               # Debug utilities and tools
├── output/              # Excel results, training logs, etc.
├── .env
├── config.cfg
├── README.md
└── requirements.txt
