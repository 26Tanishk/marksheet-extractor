# Marksheet Extraction API

This project provides a FastAPI-based backend service to extract structured information from academic marksheets.
It uses OCR to extract raw text from documents and a large language model to convert unstructured text into a validated JSON response.

## High-Level Flow

1. A marksheet file (PDF or image) is uploaded via the API.
2. OCR is applied to extract raw text from the document.
3. The extracted text is passed to an LLM for structured parsing.
4. The output is validated using Pydantic schemas.
5. A confidence score is computed based on field completeness.

## API Overview

### POST /extract
Accepts a marksheet file and returns structured data including:
- Student information
- Exam details
- Subject-wise results
- Overall result
- Confidence scores

## Confidence Scoring

The API returns a confidence score to indicate how reliable the extracted data is. Confidence is computed heuristically and exposed at field level to make uncertainty explicit.

## Project Status

The project currently focuses on correctness, clarity, and schema validation.
OCR accuracy and model tuning are intentionally kept minimal to prioritize a clean and debuggable backend design.

## Tech Stack

- FastAPI
- Pydantic
- Tesseract OCR
- Google Gemini (via API)
