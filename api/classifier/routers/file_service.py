import pdfplumber

from classifier.routers.classifier_model import TypeDoc

def txt_to_string(file_path: str) -> str:
    """Converte um arquivo .txt para string."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Erro ao ler arquivo TXT: {e}")

def pdf_to_string(file_path: str) -> str:
    """Converte um arquivo PDF para string usando pdfplumber."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text if text else "Nenhum texto extraído do PDF."
    except Exception as e:
        raise RuntimeError(f"Erro ao ler arquivo PDF: {e}")

def is_valid_pdf(file_path: str) -> bool:
    """Verifica se um arquivo é um PDF válido."""
    try:
        with open(file_path, "rb") as f:
            header = f.read(4)
        return header == b"%PDF"
    except:
        return False