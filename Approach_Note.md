## Problem Understanding

The goal of this assignment was to build an API that takes a marksheet (image or PDF) as input and returns extracted information in a structured JSON format along with confidence scores.

The main challenge is that academic marksheets do not follow a fixed structure Layouts, field placement, naming conventions, and formatting vary widely across boards and institutions. Because of this variability, the system needs to handle unstructured and noisy input while still producing a consistent and predictable output.


## System Design

I approached the problem by breaking the extraction process into clear and independent stages: file input, text extraction, structured parsing, and validation.

Keeping these stages separate was a deliberate choice. It makes the system easier to reason about, debug, and extend, especially when OCR or parsing fails.

At a high level, the flow is:

uploaded document --> OCR --> raw text --> LLM-based structuring --> schema validation --> API response

Each stage has a single responsibility and avoids leaking assumptions into the next stage.


## OCR Strategy

For text extraction, I used Tesseract OCR to convert images and PDFs into raw text.

The OCR layer is intentionally kept minimal. No layout-specific rules or document assumptions are applied at this stage. This avoids overfitting the system to a small set of sample marksheets and keeps the OCR output as close as possible to the raw document content.

OCR errors are expected and treated as an input constraint rather than something to fully eliminate.


## LLM-Based Structuring

Given the variation in marksheet layouts, a purely rule-based or regex-driven approach would be brittle and hard to generalize.

To address this, I used a large language model only for structured interpretation of OCR text. The model is constrained by a fixed schema and explicitly instructed not to guess missing values. If a field cannot be confidently identified, it is returned as null.

The LLM is not used for generation or enrichment, but strictly as a flexible parser that maps noisy text into a predefined structure.


## Schema Design

The output schema is defined using Pydantic models to enforce consistency and validation.

All fields are optional where extraction may be unreliable. This allows the API to return partial but valid results instead of failing when some information is missing.

The schema includes student details, exam metadata, subject-wise results, and overall performance information when available. This structure was chosen to balance usefulness with robustness.


## Confidence Scoring

Confidence scores are computed heuristically based on field completeness rather than model probabilities.

The goal of confidence scoring is not to claim correctness, but to make uncertainty explicit. If important fields are missing or partially extracted, the confidence score reflects that.

Confidence is exposed at a field-group level to keep the logic simple, interpretable, and aligned with the assignment requirements.


## Generalization Considerations

The system is designed to generalize to unseen marksheets by avoiding document-specific rules, fixed layouts, or hardcoded patterns.

All extraction decisions are schema-driven and assisted by the language model, allowing the API to handle new formats without retraining or manual tuning.


## Design Trade-offs

The main trade-off in this design is between extraction accuracy and system robustness.

I intentionally prioritized clarity, schema validation, and graceful failure handling over aggressive OCR tuning or layout-specific optimizations. While this may reduce extraction completeness in some cases, it improves maintainability and reduces failure modes on unfamiliar documents.


## Conclusion

This approach results in a modular backend that is easier to debug, evaluate, and extend.

Rather than optimizing for perfect extraction on a small dataset, the system focuses on transparency, consistency, and controlled use of AI to handle real-world variability.