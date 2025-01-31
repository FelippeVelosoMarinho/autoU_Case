from fastapi import HTTPException
import PyPDF2

from classifier.routers.classifier_model import TypeDoc

# Função para processar o conteúdo do arquivo com base no tipo
def process_file(file_path: str, file_type: TypeDoc) -> str:
    """Processa arquivos PDF ou TXT e retorna seu conteúdo como string."""
    if file_type == TypeDoc.PDF:
        try:
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {e}")
    
    elif file_type == TypeDoc.TXT:
        try:
            with open(file_path, "r", encoding="utf-8") as txt_file:
                return txt_file.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar TXT: {e}")
    
    raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado para processamento.")
