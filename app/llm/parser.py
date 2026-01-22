import os
import json
import re
import time
from typing import Dict, Any

import google.generativeai as genai

# Configure Gemini using environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = genai.GenerativeModel("gemini-1.5-flash")

BASE_PROMPT = """
You are an information extraction system.

Task:
Extract structured information from OCR text of an academic marksheet.

Rules:
- Return ONLY valid JSON. No explanations, no markdown, no backticks.
- Use null for missing values.
- Normalize numeric values where possible.
- Keep subject list as an array of objects.
- Include "llm_confidence" (0.0 to 1.0) indicating LLM's clarity.
- Strictly follow the schema below.

Schema example:
{
  "student_info": {
    "name": null,
    "roll_number": null,
    "registration_number": null,
    "date_of_birth": null
  },
  "exam_info": {
    "issue_date": null,
    "issue_place": null
  },
  "subjects": [
    {
      "subject_name": null,
      "marks_obtained": null,
      "maximum_marks": null,
      "grade": null,
      "result": null
    }
  ],
  "overall_result": {
    "total_marks": null,
    "maximum_marks": null,
    "percentage": null,
    "grade": null,
    "result_status": null
  },
  "llm_confidence": 0.0
}
"""

CORRECTION_PROMPT = """
Your previous response was not valid JSON. Extract ONLY the JSON that fits the schema, and nothing else.
Here is the OCR text again:
---
{ocr}
---
Return only the JSON object.
"""

# Deterministic fallback to extract a few high-signal fields when LLM parsing fails
def regex_fallback(ocr_text: str) -> Dict[str, Any]:
    def find(pattern):
        m = re.search(pattern, ocr_text, flags=re.IGNORECASE | re.MULTILINE)
        return m.group(1).strip() if m else None

    name = find(r"Name[:\-\s]*([A-Z][A-Za-z\s\.]{2,80})")
    roll = find(r"Roll(?:\s*No\.?|[:\s])\s*([A-Za-z0-9\-]+)")
    dob = (
        find(r"DOB[:\-\s]*([0-3]?\d[\/\-][01]?\d[\/\-]\d{2,4})")
        or find(r"Date of Birth[:\-\s]*([0-3]?\d[\/\-][01]?\d[\/\-]\d{2,4})")
    )
    total = find(r"Total(?:\s*Marks)?[:\-\s]*([0-9]{1,4})")
    percentage = find(r"Percentage[:\-\s]*([0-9]{1,3}(?:\.[0-9]+)?)")

    return {
        "student_info": {
            "name": name,
            "roll_number": roll,
            "registration_number": None,
            "date_of_birth": dob,
        },
        "exam_info": {},
        "subjects": [],
        "overall_result": {
            "total_marks": float(total) if total and total.isdigit() else None,
            "maximum_marks": None,
            "percentage": float(percentage) if percentage else None,
            "grade": None,
            "result_status": None,
        },
        "llm_confidence": 0.05,
    }

def extract_json_from_text(text: str) -> dict:
    """
    Attempt to safely extract a JSON object from model output.
    """
    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except Exception:
            pass

    brace_stack = 0
    start_idx = -1
    for i, ch in enumerate(text):
        if ch == "{":
            if start_idx == -1:
                start_idx = i
            brace_stack += 1
        elif ch == "}":
            brace_stack -= 1
            if brace_stack == 0 and start_idx != -1:
                try:
                    return json.loads(text[start_idx:i + 1])
                except Exception:
                    start_idx = -1

    raise ValueError("No valid JSON found")

def call_llm(prompt: str, ocr_text: str, max_tokens: int = 1024) -> str:
    content = prompt + "\n\nOCR TEXT:\n" + ocr_text
    response = MODEL.generate_content(
        content,
        generation_config={"temperature": 0, "max_output_tokens": max_tokens}
    )
    return response.text

def parse_marksheet_text(ocr_text: str) -> dict:
    attempts = 0
    last_text = ""

    while attempts < 3:
        try:
            attempts += 1

            if attempts == 1:
                response_text = call_llm(BASE_PROMPT, ocr_text)
            else:
                correction = CORRECTION_PROMPT.format(ocr=ocr_text)
                response_text = call_llm(correction, ocr_text)

            last_text = response_text
            parsed = extract_json_from_text(response_text)

            if not isinstance(parsed, dict):
                raise ValueError("Parsed output is not a dictionary")

            required_keys = {
                "student_info",
                "exam_info",
                "subjects",
                "overall_result",
                "llm_confidence",
            }

            for key in required_keys:
                parsed.setdefault(key, {} if key != "subjects" else [])

            return parsed

        except Exception:
            if attempts >= 2:
                try:
                    followup = (
                        "Previous output:\n\n"
                        f"{last_text}\n\n"
                        "Extract only the JSON matching the schema."
                    )
                    response_text = call_llm(followup, ocr_text)
                    return extract_json_from_text(response_text)
                except Exception:
                    break

            time.sleep(0.6)

    # Final fallback to guarantee a valid response instead of failing the API
    return regex_fallback(ocr_text)
