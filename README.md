# AI Data Extraction Tool

An AI-powered document entity extractor that allows users to upload multiple files (PDF, Word, or text), extract entities (Names, Emails, Organizations), and download structured Excel outputs.

Built with FastAPI + GPT (optional) + Pandas.

---

## 🚀 Features
- Upload one or multiple documents at once
- Extract Names, Emails, and Organizations
- View a preview of extracted entities
- Download structured Excel (.xlsx) output
- Auto-cleanup old files every hour
- Optional GPT-powered extraction for higher accuracy
- Background file cleanup and result logging to CSV

---

## 📂 Project Structure

```bash
AIDataExtractionTool/
├── api/
│
├── main.py
│
├── templates/
│ └── utils/, temp_uploads/, etc.
├── extractor/
│ └── text_extractor.py, file_reader.py
├── output/ (auto-generated)
├── logs/ (auto-generated)
├── .env.example
├── requirements.txt
├── render.yaml
```
---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ai-data-extraction-tool.git
cd ai-data-extraction-tool

# Set up virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env
cp .env.example .env
```

---


## 🏃 Run Locally

```bash
uvicorn api.main:app --reload --port 8000
```
Then open your browser at http://localhost:8000

