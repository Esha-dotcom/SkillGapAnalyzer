import pdfplumber
import docx

def extract_text(file):

    text = ""

    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text

    elif file.name.endswith(".txt"):
        text = file.read().decode()

    return text.lower()