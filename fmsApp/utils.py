# utils.py

from PyPDF2 import PdfReader
import pytesseract

def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file.path, "rb") as f:
        pdf_reader = PdfReader(f)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def perform_ocr(text):
    # No need to perform OCR on the text, as it's already extracted
    return text
