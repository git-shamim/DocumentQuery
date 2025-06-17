import os
import io
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file):
    """
    Extracts raw text from uploaded file.
    Supported types: PDF, DOCX, TXT, CSV
    Returns a string of the full extracted text.
    """
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return _extract_text_from_pdf(file)

    elif filename.endswith(".docx"):
        return _extract_text_from_docx(file)

    elif filename.endswith(".txt"):
        return _extract_text_from_txt(file)

    elif filename.endswith(".csv"):
        return _extract_text_from_csv(file)

    else:
        raise ValueError(f"Unsupported file format: {filename}")

def _extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def _extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def _extract_text_from_txt(file):
    content = file.read()
    return content.decode("utf-8")

def _extract_text_from_csv(file):
    df = pd.read_csv(file)
    return df.to_string(index=False)
