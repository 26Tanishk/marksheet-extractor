# Marksheet Extraction API

FastAPI-based AI document extraction pipeline for parsing academic marksheets into structured JSON using OCR + Gemini LLM.

---

## Live Demo
- API Docs: [Swagger Docs](https://marksheet-extractor-lmg0.onrender.com/docs)

## Features

- OCR-based text extraction from images and PDFs
- Schema-aligned structured JSON generation
- Confidence scoring for extracted fields
- Explicit validation and error handling
- Dockerized deployment
- FastAPI Swagger documentation
- Designed to handle noisy and layout-inconsistent OCR outputs

---

## Architecture

```text
Client Upload
      ↓
 FastAPI Endpoint
      ↓
 OCR Extraction (Tesseract)
      ↓
 Gemini LLM Structuring
      ↓
 Pydantic Validation
      ↓
 Confidence Scoring
      ↓
 Structured JSON Response
```
---

## API Demo

### Input Marksheet
<img src="https://github.com/user-attachments/assets/15ad9926-c357-4e5b-ac5d-f0f9b9245b3d" width="45%" alt="Input Marksheet" />

### Swagger Documentation
<img src="https://github.com/user-attachments/assets/7f68f4ca-cb19-4626-8026-7076b017a8b2" width="80%" alt="Swagger Docs" />


---

## Motivation

Academic marksheets vary significantly across:
- boards
- universities
- layouts
- OCR quality

Traditional regex-heavy pipelines become brittle when document formats change slightly.

This project uses a hybrid OCR + LLM pipeline where:
- OCR extracts raw document text
- Gemini LLM structures noisy text into a predefined schema
- Validation logic prevents malformed outputs
- Missing values are explicitly returned as `null`

---

## Extraction Pipeline

1. Upload marksheet (PDF/image)
2. OCR extracts raw text
3. Gemini parses text into structured schema
4. Pydantic validates output
5. Confidence score computed
6. Structured JSON returned to client

---

## Use of LLM

The LLM is used only for:
- interpreting noisy OCR text
- identifying relevant fields
- normalizing values into a fixed schema

The system is explicitly instructed:
- not to hallucinate fields
- not to infer missing values
- to return `null` when information is unclear
---

## Confidence Scoring

Confidence scores are computed heuristically using:
- completeness of student metadata
- subject-level extraction quality
- availability of overall result information

This makes extraction uncertainty explicit instead of masking partial outputs behind a generic success response.

---

## Sample Response

```json
{
  "student_info": {
    "name": "NARAYAN DEBNATH",
    "roll_number": "F06931",
    "registration_number": null,
    "date_of_birth": null
  },
  "exam_info": {
    "issue_date": null,
    "issue_place": null
  },
  "subjects": [],
  "overall_result": {
    "total_marks": 515,
    "maximum_marks": null,
    "percentage": null,
    "grade": null,
    "result_status": null
  },
  "confidence": {
    "overall_confidence": 0.21,
    "field_confidence": {
      "student_info": 0.5,
      "subjects": 0,
      "overall_result": 0.25
    }
  }
}
```
---

## Extraction Notes

The example above demonstrates the system's behavior on a noisy and layout-heavy marksheet.

Instead of hallucinating uncertain values, the API:
- returns `null` for unclear fields
- lowers confidence scores for incomplete extraction
- preserves schema consistency even under OCR uncertainty

This design prioritizes transparency and robustness over aggressive guessing.

## Deployment

- Dockerized using Docker
- Public deployment hosted on Render
- Interactive API docs available via Swagger UI

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend API | FastAPI |
| OCR Engine | Tesseract OCR |
| LLM | Google Gemini |
| Validation | Pydantic |
| Containerization | Docker |
| Deployment | Render |

---

## Design Decisions

- OCR and structuring are intentionally separated
- LLM is restricted to schema normalization only
- Invalid or incomplete fields are returned as `null`
- Explicit validation prevents malformed responses
- Failures are surfaced transparently via HTTP errors


---

## Limitations

- OCR quality directly impacts extraction accuracy
- Complex tabular subject layouts remain challenging
- Extremely noisy scans may reduce field completeness

The system prioritizes transparency and robustness over aggressive guessing.


---

## Local Setup

```bash
git clone https://github.com/26Tanishk/marksheet-extractor.git
cd marksheet-extractor

pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```


---


## Future Improvements

- Batch extraction endpoint
- Async request handling
- Bounding-box extraction
- Improved OCR benchmarking
- Multi-language support


---

