from pypdf import PdfReader
from docx import Document
import pandas as pd
import os


def extract_text(filepath):

    ext = os.path.splitext(filepath)[1].lower()

    # -------- PDF --------
    if ext == ".pdf":
        reader = PdfReader(filepath)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    # -------- DOCX --------
    if ext == ".docx":
        doc = Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    # -------- EXCEL --------
    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
        return df.to_string()

    # -------- TXT --------
    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    raise ValueError("Unsupported file type")
