import fitz  # PyMuPDF
from docx import Document
import pandas as pd
import os


def parse_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return parse_pdf(filepath)

    elif ext == ".docx":
        return parse_docx(filepath)

    elif ext == ".xlsx":
        return parse_excel(filepath)

    elif ext in [".txt", ".md"]:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file type")


# ---------- PDF ----------
def parse_pdf(filepath):
    text = ""
    doc = fitz.open(filepath)

    for page in doc:
        text += page.get_text()

    return text


# ---------- WORD ----------
def parse_docx(filepath):
    doc = Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])


# ---------- EXCEL ----------
def parse_excel(filepath):
    df = pd.read_excel(filepath)
    return df.to_string()
