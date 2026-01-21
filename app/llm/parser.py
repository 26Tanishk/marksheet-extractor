import json
import google.generativeai as genai
from app.schema.marksheet import MarksheetResponse

def configure_gemini(api_key: str):
    genai.configure(api_key=api_key)

def build_prompt(raw_text: str) -> str:
    return f"""
You are given raw OCR text extracted from an academic marksheet.

Your task is to extract structured information strictly according to the provided JSON schema.

Rules:
- Do NOT guess missing values.
- If a field is not found, set it to null.
- Do NOT calculate totals or percentages.
- Use only information explicitly present in the text.
- Output ONLY valid JSON. No explanation.

Raw OCR Text:
{raw_text}
"""


def parse_marksheet_text(
    raw_text: str,
    api_key: str
) -> MarksheetResponse:
    configure_gemini(api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = build_prompt(raw_text)

    response = model.generate_content(prompt)

    parsed_json = json.loads(response.text)
    return MarksheetResponse(**parsed_json)