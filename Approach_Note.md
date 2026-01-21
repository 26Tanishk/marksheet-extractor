## Problem Understanding
The goal of this assignment is to build an API that takes a marksheet (image or PDF) as input and returns the extracted information in JSON format along with confidence scores.

The main difficulty is that marksheets do not follow a fixed structure. Layouts, formats, and field placement can vary a lot, so the solution needs to handle unstructured data while still producing a consistent output.



## System Design
I designed the system by breaking the extraction process into simple and clear stages: file input, text extraction, structured parsing, and validation.
Keeping these stages separate makes the system easier to understand, debug, and modify if needed

Overall, the flow is:
uploaded document -> OCR -> raw text -> LLM-based structuring -> schema validation -> API response.



## OCR Strategy
For text extraction, I used Tesseract OCR to convert images and PDFs into raw text.

The OCR layer is intentionally kept simple and limited to text extraction only. No document-specific rules or layout assumptions are applied at this stage to avoid overfitting to any particular marksheet format.



## LLM-Based Structuring
Since marksheets vary significantly in layout and formatting, rule-based parsing would be brittle and difficult to generalize.

To address this, I used a large language model to interpret the raw OCR text and map it into a predefined JSON schema. This allows the system to remain flexible across different institutions and exam formats.



## Schema Design
The output schema is defined using Pydantic models to enforce structure and validation.

All fields are designed to be optional where extraction may be unreliable, ensuring that partial results can still be returned without breaking the API contract.

The schema includes student information, exam metadata, subject-wise results, overall performance, and document-level metadata such as issue date and place when available.



## Confidence Scoring
Confidence scores are computed heuristically based on field completeness rather than model probabilities.

The purpose of confidence scoring is not to claim accuracy, but to clearly indicate uncertainty. This helps downstream users understand how reliable each extracted field is.
Confidence is exposed at field level to align with the assignment requirements while keeping the computation simple and explainable.



## Generalization Considerations
The system is designed to generalize to unseen marksheets by avoiding document-specific rules, fixed layouts, or hardcoded patterns.

All extraction decisions are schema-driven and model-assisted, allowing the API to handle diverse formats without tuning to sample data.



## Design Tradeoffs
The primary tradeoff in this design is between extraction accuracy and system robustness.

I prioritized clarity, schema validation, and generalization over aggressive OCR tuning or layout-specific optimizations, as these would reduce maintainability and increase failure modes on unseen documents.



## Conclusion
This approach results in a clean, modular backend that is easy to extend, debug, and evaluate.
The design focuses on correctness and transparency rather than over-optimization.