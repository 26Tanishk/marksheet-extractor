from io import BytesIO
from PIL import Image

import pytesseract
from pdf2image import convert_from_bytes


def extract_text_from_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pages = convert_from_bytes(pdf_bytes)
    return "\n".join(extract_text_from_image(p) for p in pages)


def extract_raw_text(file_bytes: bytes, file_type: str) -> str:
    # OCR layer is intentionally kept minimal to avoid layout assumptions
    if file_type == "pdf":
        return extract_text_from_pdf(file_bytes)

    image = Image.open(BytesIO(file_bytes))
    return extract_text_from_image(image)
