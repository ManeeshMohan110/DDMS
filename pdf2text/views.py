from django.shortcuts import render
from django.http import HttpResponse
from pdf2image import convert_from_bytes
import pytesseract
from docx import Document

def home(request):
    return render(request, 'pdf2text/home.html')

def convert_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        images = convert_from_bytes(pdf_file.read())
        
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image, lang='mal+eng')  # Specify Malayalam and English
        
        # Create a new Word document
        doc = Document()
        
        # Add the extracted text to the document
        doc.add_paragraph(text)
        
        # Prepare response for downloading the Word document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="converted.docx"'
        
        # Save the document to the HttpResponse
        doc.save(response)
        
        return response
    
    return HttpResponse("Error converting PDF")
