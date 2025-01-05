def load_pdf(file_path):
    # 加载PDF文件并返回文件对象
    from PyPDF2 import PdfReader
    reader = PdfReader(file_path)
    return reader

def extract_text(pdf_reader):
    # 从PDF读取器中提取文本
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()