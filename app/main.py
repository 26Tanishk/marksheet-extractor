from fastapi import FastAPI, UploadFile, File, HTTPException
import os

from app.ocr.extractor import extract_raw_text
from app.llm.parser import parse_marksheet_text
from app.schema.marksheet import MarksheetResponse
from app.utils.confidence import compute_confidence


app = FastAPI(
    title="Marksheet Extraction API",
    description="API to extract structured data from marksheets",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "service running",
    }


@app.post("/extract", response_model=MarksheetResponse)
async def extract_marksheet(file: UploadFile = File(...)):
    """
    Extract structured data from a marksheet file (PDF or image).
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded",
        )

    file_bytes = await file.read()
    filename = file.filename.lower()

    # --- OCR STEP ---
    try:
        if filename.endswith(".pdf"):
            raw_text = extract_raw_text(file_bytes, file_type="pdf")
        else:
            raw_text = extract_raw_text(file_bytes, file_type="image")
    except Exception:
        # Hosted environments may not support OCR dependencies
        raise HTTPException(
            status_code=501,
            detail="OCR backend not available in this environment",
        )

    if not raw_text or not raw_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text could be extracted from the document",
        )

    # --- LLM STEP ---
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="LLM service not configured",
        )

    try:
        result = parse_marksheet_text(raw_text, api_key)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Failed to structure extracted text using LLM",
        )

    # --- CONFIDENCE SCORING ---
    confidence = compute_confidence(
        result.student_info,
        result.subjects,
        result.overall_result,
    )

    result.confidence = confidence
    return result
