import os
import sys

try:
    import pdfplumber
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
    import pdfplumber

folder = r"c:\Users\jamic\新增資料夾"
pdf_path = os.path.join(folder, "ilovepdf_merged.pdf")

try:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for i, page in enumerate(pdf.pages[:15]):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        with open(os.path.join(folder, "pdf_content_plumber.txt"), "w", encoding="utf-8") as f:
            f.write(text)
        print("Success extracting with pdfplumber, length:", len(text))
except Exception as e:
    print(f"Error PDF: {e}")
