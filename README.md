<<<<<<< HEAD
# 🧠 AIDataExtractionTool

This tool extracts **names**, **emails**, and **organization names** from large batches of files (PDF, DOCX, TXT) using NLP — ideal for analyzing business documents, reports, forms, and more.

---

## 🔍 Features
- 📂 Batch processing for PDF, DOCX, and TXT files
- 🧠 AI-powered NER using spaCy (custom or pre-trained model)
- 📊 Outputs results to Excel for review or reporting
- 🧾 Built-in logging to `logs/` for easier debugging and traceability
- 🔁 Easy to retrain with new data using `training/` scripts
- 📧 Finds and validates email addresses
- 📊 Outputs results to a single Excel file
- 🌱 Simple config using `.env`

---

### 💡 Use Cases
- Resume parsing for recruiters
- Archiving historical or legal documents
- Lead generation (email + org matching)
- Automating manual data extraction tasks

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash

git clone https://github.com/your-username/AIDataExtractionTool.git
cd AIDataExtractionTool
```


### 2. Create and Activate a Virtual Environment

```
python -m venv venv
```

### Windows
```
venv\Scripts\activate
```

### macOS/Linux

```
source venv/bin/activate
```
### 3. Install Requirements
```bash

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### 📦 Dependencies
```angular2html
spaCy
pdfplumber
python-docx
pandas
openpyxl
python-dotenv
```
Install with:
```
pip install -r requirements.txt
```

### 4. Set Up the .env File

Create a .env file based on the .env.example:

```
cp .env.example .env
```

Then modify the values:
```angular2html
INPUT_FOLDER=./input_files
OUTPUT_FOLDER=./output
```

▶️ Running the Tool


```
python main.py
```

The script will:
- Load all supported files from INPUT_FOLDER
- Extract names, emails, and organization entities
- Output results into OUTPUT_FOLDER/extracted_data.xlsx



## 📊 Example Output
| Filename          | Names              | Emails               | Organizations        |
|-------------------|--------------------|----------------------|----------------------|
| contact_list.pdf  | John Doe, Jane     | jane@abc.com         | ABC Corp, Global Inc |
| report.docx       |                    | contact@biz.org      | BizOrg, Horizon Inc  |

### 🔧 Project Structure

```angular2html
AIDataExtractionTool/
│
├── extractor/                 # Text extraction and NLP processing
│   └── text_extractor.py
│   └── file_reader.py
│
├── utils/                     # Utility functions
│   └── file_handler.py
│   └── export_excel.py
│   └── logger_config.py
│
├── training/                 # Training scripts and annotated data
│   ├── train_model.py
│   ├── build_spacy_data.py
│   ├── training_data.py
│   └── training_data.spacy
│
├── models/                   # Saved custom NER models
│   └── trained/
│
├── debug/                    # Diagnostic scripts
│   ├── inspect_spacy_file.py
│   ├── debug_offsets.py
│
├── input_files/              # Example input data
├── output/                   # Exported Excel results
├── logs/                     # Log files
├── .env                      # Environment variables (INPUT_FOLDER, OUTPUT_FOLDER)
├── main.py                   # Entry point script
├── README.md                 # Project documentation
├── config.cfg                # spaCy training config
```

## 🧠 Training a Custom Model
You can train your own NER model with updated data using:
```
python training/train_model.py
```
To convert annotated data into `.spacy` format:
```
python training/build_spacy_data.py
```
Edit your examples in `training/training_data.py` to fit your real document types.

## 📈 Future Plans
- Web-based interface for uploads
- Confidence scoring and result filtering
- Retrain models dynamically with labeled data

## 📜 License
MIT — Free to use and modify for commercial or personal projects.

## 👨‍💻 Author
**Paul-Michael Smith**

Freelance Automation Developer

🔗 Upwork Profile
🔗 GitHub
🔗 LinkedIn
=======
# document-entity-extractor
>>>>>>> 291eec73b058823c1a92a9e9d0c403089e5394b3
