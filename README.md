\# Marksheet Extraction API



A FastAPI-based backend service to extract structured data from academic marksheets using OCR and LLM-based post-processing.



---



\## Overview



This project aims to extract relevant fields (student details, subjects, marks, totals, etc.) from marksheet documents (PDFs or images) and return them in a structured JSON format.



---



\## Tech Stack



\- Backend: FastAPI (Python)

\- OCR: Tesseract OCR

\- LLM: Google Gemini



---



\## Project Structure



app/

├── api/

├── ocr/

├── llm/

├── schema/

├── utils/

└── main.py




---



\## Current Status



\- \[x] Project setup completed

\- \[x] FastAPI skeleton implemented

\- \[ ] JSON schema design

\- \[ ] OCR pipeline

\- \[ ] LLM-based structuring

\- \[ ] Confidence scoring

\- \[ ] Extraction endpoint



---



\## Planned API Endpoints



\- `GET /` — Health check

\- `POST /extract` — Extract structured data from marksheet



---



\## Notes



\- This project focuses on generalization across different marksheet formats.

\- The implementation is incremental and schema-driven.

