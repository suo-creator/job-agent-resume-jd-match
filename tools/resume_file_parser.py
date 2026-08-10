from langchain.tools import tool
import os
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

# Windows必须配置tesseract路径，改成你本地安装路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@tool
def parse_resume_file(file_path: str) -> str:
    """
    解析简历文件，支持pdf、docx、png、jpg图片，返回纯文本简历内容
    参数：
        file_path：本地临时文件完整路径
    返回：
        提取后的简历全文文本
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    elif ext == ".docx":
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext in [".jpg", ".jpeg", ".png"]:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang="chi_sim+eng")

    else:
        raise Exception("仅支持pdf/docx/jpg/png简历文件")

    return text