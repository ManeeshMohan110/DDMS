# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from PyPDF2 import PdfReader
# from pytesseract import TesseractError  # Import TesseractError here
# import pytesseract

# from .models import Post

# @receiver(post_save, sender=Post)
# def save_pdf_content(sender, instance, created, **kwargs):
#     if instance.file_path and created:  # Check if the instance is newly created
#         # Convert PDF to text using PyPDF2
#         pdf_text = extract_text_from_pdf(instance.file_path)
        
#         # Perform OCR on the extracted text
#         ocr_text = perform_ocr(pdf_text)
        
#         # Save the OCR text to the pdf_content field
#         instance.pdf_content = ocr_text
#         instance.save(update_fields=['pdf_content'])  # Exclude pdf_content from being saved again triggering the recursion

# def extract_text_from_pdf(pdf_file):
#     text = ""
#     with open(pdf_file.path, "rb") as f:
#         pdf_reader = PdfReader(f)
#         num_pages = len(pdf_reader.pages)
#         for page_num in range(num_pages):
#             page = pdf_reader.pages[page_num]
#             text += page.extract_text()
#     return text

# # import pytesseract

# def perform_ocr(text):
#     try:
#         # Perform OCR using pytesseract
#         ocr_text = pytesseract.image_to_string(text, config='--psm 6')
#         return ocr_text
#     except TesseractError as e:
#         # Log the error or handle it gracefully
#         print(f"Error during OCR: {e}")
#         return ""
#     except UnicodeDecodeError as decode_error:
#         # Handle the Unicode decode error by replacing invalid bytes
#         print(f"Unicode Decode Error: {decode_error}")
#         return text











# # Add necessary imports
# # from django.db.models.signals import post_save
# # from django.dispatch import receiver
# # from .models import Post
# # from .utils import extract_text_from_pdf, perform_ocr

# # @receiver(post_save, sender=Post)
# # def save_pdf_content(sender, instance, created, **kwargs):
# #     if instance.file_path and created:  # Check if the instance is newly created
# #         # Convert PDF to text using PyPDF2
# #         pdf_text = extract_text_from_pdf(instance.file_path)
        
# #         # Save the extracted text to the pdf_content field
# #         instance.pdf_content = pdf_text
# #         instance.save(update_fields=['pdf_content'])  # Exclude pdf_content from being saved again triggering the recursion






from django.db.models.signals import post_save
from django.dispatch import receiver
from PyPDF2 import PdfReader
from pytesseract import TesseractError
import pytesseract
from pdf2image import convert_from_path

from .models import Post

@receiver(post_save, sender=Post)
def save_pdf_content(sender, instance, created, **kwargs):
    if instance.file_path and created:  # Check if the instance is newly created and has a file attached
        if instance.file_path.name.lower().endswith('.pdf'):  # Check if the file is a PDF
            # Convert each page of the PDF to an image
            pdf_path = instance.file_path.path
            images = convert_from_path(pdf_path)

            # Perform OCR on each image and extract the content
            content = ''
            for image in images:
                extracted_text_malayalam = pytesseract.image_to_string(image, lang='mal')
                extracted_text_english = pytesseract.image_to_string(image, lang='eng')
                content +=  extracted_text_english + '\n' + extracted_text_malayalam + '\n' 

            # Save the OCR text to the pdf_content field
            instance.pdf_content = content
            instance.save()

def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as f:
        pdf_reader = PdfReader(f)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def perform_ocr(text):
    try:
        # Perform OCR using pytesseract for English
        ocr_text_eng = pytesseract.image_to_string(text, lang='eng')
        # Perform OCR using pytesseract for Malayalam
        ocr_text_mal = pytesseract.image_to_string(text, lang='mal')
        # Combine both English and Malayalam text
        ocr_text = ocr_text_eng + '\n' + ocr_text_mal
        return ocr_text
    except TesseractError as e:
        # Log the error or handle it gracefully
        print(f"Error during OCR: {e}")
        return ""
