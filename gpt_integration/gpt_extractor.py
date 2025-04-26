import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# ───────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: GPT-backed entity extraction (PERSON, ORG, EMAIL) from text
# Usage: Import and call extract_entities_with_gpt(text)
# ───────────────────────────────────────────────────────────────────────

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

def extract_entities_with_gpt(text):
    prompt = f"""
You are a helpful assistant that extracts information from text.
From the following document, extract all PERSON names, ORGANIZATIONS, and EMAILS.
Return them in JSON format like this:
{{
  "person": ["Name1", "Name2"],
  "organization": ["Org1", "Org2"],
  "email": ["email1@example.com"]
}}

Document:
{text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Change model for better accuracy
            messages=[
                {"role": "system", "content": "You extract structured data from unstructured text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print(f"❌ Error during GPT extraction: {e}")
        return {"person": [], "organization": [], "email": []}
