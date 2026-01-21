from typing import Union
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract raw text from a PIL Image using Tesseract OCR.
    """
    text = pytesseract.image_to_string(image)
    return text


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Convert PDF pages to images and extract text from each page.
    """
    pages = convert_from_bytes(pdf_bytes)
    extracted_text = []

    for page in pages:
        page_text = extract_text_from_image(page)
        extracted_text.append(page_text)

    return "\n".join(extracted_text)



def extract_raw_text(
    file_bytes: bytes,
    file_type: str
) -> str:
    """
    Unified OCR entry point.
    file_type: 'pdf' or 'image'
    """
    if file_type == "pdf":
        return extract_text_from_pdf(file_bytes)

    image = Image.open(file_bytes)
    return extract_text_from_image(image)



