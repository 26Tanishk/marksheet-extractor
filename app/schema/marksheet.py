from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class StudentInfo(BaseModel):
    name: Optional[str] = None
    roll_number: Optional[str] = None
    registration_number: Optional[str] = None
    date_of_birth: Optional[str] = None


class ExamInfo(BaseModel):
    issue_date: Optional[str] = None
    issue_place: Optional[str] = None


class SubjectResult(BaseModel):
    subject_name: str
    marks_obtained: Optional[float] = None
    maximum_marks: Optional[float] = None
    grade: Optional[str] = None
    result: Optional[str] = None


class OverallResult(BaseModel):
    total_marks: Optional[float] = None
    maximum_marks: Optional[float] = None
    percentage: Optional[float] = None
    grade: Optional[str] = None
    result_status: Optional[str] = None


class ConfidenceScore(BaseModel):
    overall_confidence: float
    field_confidence: Optional[Dict[str, Any]] = None


class MarksheetResponse(BaseModel):
    student_info: StudentInfo
    exam_info: ExamInfo
    subjects: List[SubjectResult]
    overall_result: OverallResult
    confidence: Optional[ConfidenceScore] = None
