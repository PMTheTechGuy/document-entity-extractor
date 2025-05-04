# AI Data Extraction Tool

🚀 Upload documents → Extract Names, Emails, and Organizations → Download structured Excel results instantly.  
Built with **FastAPI**, **Pandas**, and optional **GPT-enhanced** extraction.  
Deployed live on **Render**.

---

## ✨ Features

- ✅ Upload PDF, DOCX, and TXT documents
- ✅ Extract **Names**, **Emails**, and **Organizations**
- ✅ Multi-file uploads supported (combines results into one Excel)
- ✅ Clean and organized Excel file download (`.xlsx`)
- ✅ Supports both **local entity extraction** and **GPT-enhanced** extraction
- ✅ Automatic fallback if custom model is missing
- ✅ Deployed online via [Render](https://render.com/)

---

## 📸 Screenshots

### Upload Page
<img src = api/static/Upload_PageWith_item.png width = 675 height = 675 alt = Upload Page>

### Extraction Results Page
<img src = api/static/ExtractionResultsPage.png width = 675 height = 675 alt = Results Page>

---

## 🚀 Live Demo

> 🟢 [Visit the Live App Here](https://ai-data-extraction-tool.onrender.com/)  

---

## ⚙️ Technologies Used

- Python 3.11
- FastAPI
- Uvicorn
- Pandas
- spaCy
- OpenAI API (optional GPT-enhancement)
- openpyxl (for Excel export)

---

## 🛠 Local Development Setup

Clone the repository:

```bash
git clone https://github.com/PMTheTechGuy/document-entity-extractor.git
cd document-entity-extractor
```
Install dependencies:

```bash
pip install -r requirements.txt
```

Set up your environment variables:

Create a `.env` file based on `.env.example`.

```bash
cp .env.example .env
```
Start the server locally:

```bash
uvicorn api.main:app --reload
```

---

## 🌍 Deployment

This app is deployed on Render.

You can deploy your own version in one click:

---
## 📦 Folder Structure

```php
api/             # FastAPI backend
├── templates/   # HTML templates (upload form, results page)
├── static/      # Static files
├── temp_uploads/ # Temporary uploaded files
├── temp_outputs/ # Temporary generated outputs
utils/           # Helper modules (export, logging, etc.)
extractor/       # File reading and entity extraction
gpt_integration/ # GPT-enhanced extraction
output/          # Exported Excel files
logs/            # Application logs
```
---

## 📦 Features

- **Multi-file Upload**: Upload one or more `.pdf`, `.docx`, or `.txt` files for processing.
- **Entity Extraction**: Automatically identifies and extracts:
  - People (names)
  - Emails
  - Organizations
- **Results Summary**: Displays a summary of total files processed, and the number of names, emails, and organizations found.
- **CSV & Excel Export**: Download extracted data in `.csv` or `.xlsx` format.
- **Auto Cleanup**: Temporary files that are older than one hour will be automatically deleted.
- **Error Handling**: User interface for handling invalid uploads, unsupported file types, and extraction failures.
---

## 🚧 Coming Soon
- Daily upload limits per user or IP (via database tracking)
- Admin dashboard to review processed data
- File size limit configuration in .env

---
### 🙌 Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)

- [spaCy](https://spacy.io/)

- [OpenAI](https://openai.com/)

- [Render](https://render.com/)

---

## 📫 Contact

Built with passion by [PM The Tech Guy](https://github.com/PMTheTechGuy).

Please don't hesitate to reach out or share your ideas!

---
