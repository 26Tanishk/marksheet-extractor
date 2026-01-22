# Marksheet Extraction API

I built this project as a backend service to extract structured information from academic marksheets.
The goal was not to perfectly extract every field, but to design a robust and debuggable pipeline that can handle noisy and inconsistent documents.

The service exposes a FastAPI endpoint that accepts a marksheet (PDF or image) and returns a structured JSON response.

---

## Motivation

Academic marksheets vary significantly across boards, years, and layouts.  
Simple rule-based parsing or regex approaches break quickly when OCR output changes slightly.

Instead of hardcoding formats, I chose a hybrid approach:
- OCR is used only to extract raw text
- A language model is used strictly to map that noisy text into a predefined schema

The system is explicitly designed **not to guess missing values**.

---

## High-Level Flow

1. A marksheet file (PDF or image) is uploaded to the API
2. OCR (Tesseract) extracts raw text from the document
3. The extracted text is passed to an LLM for schema-aligned parsing
4. The output is validated using Pydantic models
5. A confidence score is computed based on field completeness

---

## API Overview

### `POST /extract`

Accepts a marksheet file and returns structured data including:
- Student information
- Exam metadata
- Subject-wise results (if available)
- Overall result
- Confidence scores

The API always returns a valid JSON response or a clear error message when extraction fails.

---

## Use of LLM

The language model is **not** used to generate content or infer missing information.

It is used only to:
- Interpret noisy OCR output
- Identify relevant fields
- Normalize values into a fixed schema

The prompt explicitly instructs the model to return `null` when information is missing or unclear.

---

## Confidence Scoring

Extraction uncertainty is made explicit through a confidence score.

Confidence is computed heuristically based on:
- Presence of student-level fields
- Completeness of subject entries
- Availability of overall result fields

This avoids hiding partial or unreliable extraction behind a single “successful” response.

---

## Limitations

- OCR quality directly impacts extraction accuracy
- Subject-wise extraction varies significantly across marksheet formats
- The system prioritizes robustness and transparency over completeness

These trade-offs were intentional.

---

## Tech Stack

- FastAPI
- Pydantic
- Tesseract OCR
- Google Gemini API

---

## Execution Notes

- The full OCR + PDF pipeline works locally when system dependencies (Tesseract, Poppler) are available
- Docker is used to provide a reproducible execution environment
- OCR and parsing failures are surfaced explicitly via HTTP responses instead of silent fallbacks

---

## Testing

A small set of publicly available marksheet samples was used for local testing to validate different layouts and OCR quality levels.
