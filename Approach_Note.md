# Approach Note

## Problem Overview

The task was to build an API that accepts a marksheet (image or PDF) and returns extracted information in structured JSON format along with confidence scores.

One of the main difficulties is that marksheets are highly inconsistent across different boards and universities. Field names, layouts, subject tables, and formatting vary a lot, so a fixed rule-based approach becomes unreliable very quickly.

The system therefore needed to work on noisy and semi-structured input while still producing a predictable response format.

---

## Overall Approach

I divided the pipeline into separate stages:

document upload → OCR extraction → text structuring → validation → JSON response

Each stage handles a specific responsibility independently.

This separation made the system easier to debug during development because OCR failures, parsing issues, and schema problems could be inspected separately instead of being tightly coupled together.

---

## OCR Layer

Tesseract OCR was used to extract raw text from images and PDFs.

I intentionally kept the OCR stage simple and avoided adding layout-specific rules or hardcoded extraction patterns. The goal was to avoid overfitting the pipeline to a small set of sample marksheets.

OCR quality varies significantly depending on:
- scan clarity
- document resolution
- table structure
- text alignment

Because of this, OCR mistakes are treated as an expected limitation of the input rather than something fully eliminated.

---

## LLM-Based Parsing

Instead of relying only on regex or fixed rules, I used Gemini to convert noisy OCR text into a structured schema.

The language model is not used to generate or infer missing information. Its role is limited to:
- identifying relevant fields
- mapping values into the expected schema
- handling layout variation across documents

The prompt explicitly instructs the model to return `null` for unclear or missing fields rather than guessing values.

This helped keep the API response more predictable when OCR quality was poor.

---

## Schema Validation

Pydantic models were used to validate and structure the final response.

The schema includes:
- student information
- exam metadata
- subject-wise marks
- overall result details

Many fields are optional because extraction quality can vary between documents. Returning partial but valid JSON responses was preferred over failing the request completely.

---

## Confidence Scoring

Confidence scores are calculated heuristically using extraction completeness.

The score mainly depends on:
- availability of student-level fields
- extraction of subject data
- presence of overall result information

The intention was not to measure absolute correctness, but to expose extraction reliability in a simple and interpretable way.

---

## Generalization Strategy

The system was designed to work on unseen marksheet formats without depending heavily on hardcoded layouts.

To support this:
- OCR output is kept generic
- parsing is schema-driven
- document-specific rules are avoided wherever possible

This improves flexibility across different boards and institutions, although extraction quality still depends heavily on OCR quality.

---

## Trade-offs

A major trade-off in the project was between extraction completeness and system reliability.

I chose to prioritize:
- schema consistency
- transparent failure handling
- predictable API responses

instead of aggressively forcing extraction results from noisy OCR data.

Because of this, some fields may remain `null` on difficult documents, but the API still returns a valid and interpretable response.

---

## Conclusion

The final system focuses more on robustness and maintainability than perfect extraction accuracy.

The pipeline is modular, easier to debug, and flexible enough to handle different marksheet formats without relying heavily on document-specific rules.
