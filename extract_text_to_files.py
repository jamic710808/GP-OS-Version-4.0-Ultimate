import os
import docx

folder = r"c:\Users\jamic\新增資料夾"

try:
    doc = docx.Document(os.path.join(folder, "PowerBI_毛利分析完整知識報告.docx"))
    text_docx = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
    with open(os.path.join(folder, "docx_content.txt"), "w", encoding="utf-8") as f:
        f.write(text_docx)
except Exception as e:
    print(f"Error DOCX: {e}")

try:
    import fitz
    pdf = fitz.open(os.path.join(folder, "ilovepdf_merged.pdf"))
    text_pdf = ""
    for i in range(min(50, len(pdf))): # Extract up to 50 pages to get a good overview
        text_pdf += pdf[i].get_text() + "\n"
    with open(os.path.join(folder, "pdf_content.txt"), "w", encoding="utf-8") as f:
        f.write(text_pdf)
except Exception as e:
    print(f"Error PDF: {e}")
