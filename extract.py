import os
import sys

try:
    import docx
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx", "PyMuPDF"])
    import docx

folder = r"c:\Users\jamic\新增資料夾"

print("--- DOCX ---")
try:
    doc = docx.Document(os.path.join(folder, "PowerBI_毛利分析完整知識報告.docx"))
    text_docx = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
    print(text_docx[:3000])
except Exception as e:
    print(f"Error DOCX: {e}")

print("\n--- PDF ---")
try:
    import fitz
    pdf = fitz.open(os.path.join(folder, "ilovepdf_merged.pdf"))
    text_pdf = ""
    for i in range(min(5, len(pdf))):
        text_pdf += pdf[i].get_text() + "\n"
    print(text_pdf[:4000])
except Exception as e:
    print(f"Error PDF: {e}")
