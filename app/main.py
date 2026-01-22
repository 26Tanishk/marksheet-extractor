from fastapi import FastAPI, UploadFile, File, HTTPException

from app.ocr.extractor import extract_raw_text
from app.llm.parser import parse_marksheet_text
from app.utils.confidence import compute_confidence
from app.schema.marksheet import (
    MarksheetResponse,
    StudentInfo,
    ExamInfo,
    SubjectResult,
    OverallResult,
)

app = FastAPI(
    title="Marksheet Extraction API",
    description="API to extract structured data from marksheets",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "service running"}


@app.post("/extract", response_model=MarksheetResponse)
async def extract_marksheet(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_bytes = await file.read()
    filename = file.filename.lower()

    try:
        if filename.endswith(".pdf"):
            raw_text = extract_raw_text(file_bytes, "pdf")
        else:
            raw_text = extract_raw_text(file_bytes, "image")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to extract text")

    if not raw_text.strip():
        raise HTTPException(status_code=422, detail="No readable text found")

    # Parse OCR text into a structured representation
    try:
        structured = parse_marksheet_text(raw_text)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to parse extracted text")

    student = StudentInfo(**structured.get("student_info", {}))
    exam = ExamInfo(**structured.get("exam_info", {}))

    subjects = [
        SubjectResult(**s)
        for s in structured.get("subjects", [])
    ]

    overall = OverallResult(**structured.get("overall_result", {}))

    confidence = compute_confidence(
        student=student,
        subjects=subjects,
        overall=overall,
        llm_confidence=structured.get("llm_confidence", 0.5),
    )

    return MarksheetResponse(
        student_info=student,
        exam_info=exam,
        subjects=subjects,
        overall_result=overall,
        confidence=confidence,
    )
