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
- ✅ Automatic fallback if the custom model is missing
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
If you encounter an issue loading the application on `HTTP://localhost:8000`.

Quit the application using `Ctrl + C` and start the server on port `8001`.

```bash
uvicorn api.main:app --reload --port 8001
```
---

## 🧠 OpenAI Key Setup (Optional for GPT Extraction)

This app supports two extraction modes:

- 🧠 GPT-enhanced extraction (more accurate, slower, uses OpenAI API)

- ⚡ Local spaCy model extraction (faster, free, no external API calls)

By default, the app will fall back to spaCy if no OpenAI key is provided and the `USE_GPT_EXTRACTION` is set to `False`.

### Setting Up OpenAI GPT Extraction (Optional)

#### 1. In your `.env` file, add your OpenAI API Key:

```env
OPENAI_API_KEY=your-real-openai-api-key-here
```
#### 2. Save the `.env` file.

#### 3. Restart the FastAPI server:

```bash
uvicorn api.main:app --reload
```

- ✅ If a key is provided, the app will automatically use GPT for extractions.
- ✅ If no key is provided or an API error occurs, the app will fall back to using spaCy.

---

## ⚙️ Controlling GPT Extraction Mode

In your `.env` file, you can control whether the app uses GPT or local spaCy extraction:
```
USE_GPT_EXTRACTION=True
```
- ✅ True → Use GPT extraction (requires valid OpenAI API key)

- ✅ False → Force local spaCy extraction, even if API key is present

Restart the server after changing the `.env` settings.
```
uvicorn api.main:app --reload
```

The app will detect this automatically at runtime.

---

## 🌍 Deployment

This app is deployed on [Render](https://render.com/).

You can deploy your version in one click.

---
## 📦 Folder Structure

```php
api/             # FastAPI backend
├── templates/   # HTML templates (upload form, results page)
├── static/      # Static files
utils/           # Helper modules (export, logging, etc.)
extractor/       # File reading and entity extraction
gpt_integration/ # GPT-enhanced extraction
output/          # Exported Excel files
logs/            # Application logs
```
---

### 🙌 Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)

- [spaCy](https://spacy.io/)

- [OpenAI](https://openai.com/)

- [Render](https://render.com/)

---

## 📫 Contact

Crafted with dedication by 
[PM The Tech Guy](https://github.com/PMTheTechGuy).


Please don't hesitate to reach out or share your ideas!

---
