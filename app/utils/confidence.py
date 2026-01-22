from typing import List
from app.schema.marksheet import (
    StudentInfo,
    SubjectResult,
    OverallResult,
    ConfidenceScore,
)


def completeness_score(values: List[object]) -> float:
    if not values:
        return 0.0

    present = sum(1 for v in values if v not in (None, "", []))
    return present / len(values)


def student_info_confidence(student: StudentInfo) -> float:
    fields = [
        student.name,
        student.roll_number,
        student.registration_number,
        student.date_of_birth,
    ]
    return completeness_score(fields)


def subjects_confidence(subjects: List[SubjectResult]) -> float:
    if not subjects:
        return 0.0

    subject_scores = []
    for subject in subjects:
        fields = [
            subject.subject_name,
            subject.marks_obtained,
            subject.grade,
        ]
        subject_scores.append(completeness_score(fields))

    return sum(subject_scores) / len(subject_scores)


def overall_result_confidence(overall: OverallResult) -> float:
    fields = [
        overall.total_marks,
        overall.percentage,
        overall.grade,
        overall.result_status,
    ]
    return completeness_score(fields)


def compute_confidence(
    student: StudentInfo,
    subjects: List[SubjectResult],
    overall: OverallResult,
    llm_confidence: float,
) -> ConfidenceScore:

    student_score = student_info_confidence(student)
    subjects_score = subjects_confidence(subjects)
    overall_score = overall_result_confidence(overall)

    # Combine field completeness with LLM-reported clarity
    overall_confidence = (
        0.4 * student_score +
        0.4 * subjects_score +
        0.2 * llm_confidence
    )

    return ConfidenceScore(
        overall_confidence=round(overall_confidence, 2),
        field_confidence={
            "student_info": round(student_score, 2),
            "subjects": round(subjects_score, 2),
            "overall_result": round(overall_score, 2),
        },
    )
