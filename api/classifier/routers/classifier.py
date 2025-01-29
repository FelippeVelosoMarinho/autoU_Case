from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from enum import Enum
from typing import Union
import PyPDF2
import os

# Criação do APIRouter
router = APIRouter(prefix="/classifier")

# Definição de Enum para classificação de produtividade
class IsProductive(str, Enum):
    PRODUCTIVE = "PRODUCTIVE"
    IMPRODUCTIVE = "IMPRODUCTIVE"

# Definição de Enum para os tipos de documentos suportados
class TypeDoc(str, Enum):
    STR = "STR"
    PDF = "PDF"
    TXT = "TXT"

# DTO para o response
class Classifier(BaseModel):
    msg: Union[str, UploadFile]  # Pode ser uma string ou arquivo enviado
    type: TypeDoc  # Tipo do documento

# Função para processar o conteúdo do arquivo com base no tipo
def process_file(file_path: str, file_type: TypeDoc) -> str:
    """
    Processa o conteúdo do arquivo com base no tipo especificado.

    - `file_path`: Caminho para o arquivo.
    - `file_type`: Tipo do arquivo (PDF ou TXT).

    Retorna o conteúdo do arquivo como string.
    """
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
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado para processamento.")

# Rota para leitura do conteúdo
@router.post("/read", response_model=str)
async def read(msg: Union[str, UploadFile], type: TypeDoc) -> str:
    """
    Lê o conteúdo do arquivo com base no tipo fornecido.

    - `msg`: String direta ou arquivo enviado (UploadFile).
    - `type`: Tipo do documento (STR, PDF ou TXT).
    
    Retorna o conteúdo do arquivo como string.
    """
    if type == TypeDoc.STR:
        # Caso seja uma string direta
        if isinstance(msg, str):
            return msg
        else:
            raise HTTPException(status_code=400, detail="Esperava-se uma string para o tipo STR.")

    elif type in [TypeDoc.PDF, TypeDoc.TXT]:
        # Caso seja um arquivo enviado
        if isinstance(msg, UploadFile):
            file_location = f"temp_{msg.filename}"  # Salva o arquivo em local temporário
            with open(file_location, "wb") as temp_file:
                temp_file.write(await msg.read())  # Lê o conteúdo do arquivo enviado
            
            # Processa o arquivo e retorna o conteúdo
            content = process_file(file_location, type)
            
            # Remove o arquivo temporário
            os.remove(file_location)
            return content
        else:
            raise HTTPException(status_code=400, detail=f"Esperava-se um arquivo para o tipo {type}.")

    else:
        raise HTTPException(status_code=400, detail="Tipo inválido fornecido.")

# Função para classificação da produtividade (template criado)
def classify(msg: str) -> IsProductive:
    """
    Classifica a mensagem como PRODUCTIVE ou IMPRODUCTIVE.

    - `msg`: Conteúdo a ser classificado.
    
    Retorna uma enumeração `IsProductive`.
    """
    # Template para a lógica de classificação (implementar depois)
    if len(msg.strip()) > 0:
        return IsProductive.PRODUCTIVE
    else:
        return IsProductive.IMPRODUCTIVE

# Rota para responder com uma classificação (template criado)
@router.get("/answer", response_model=str)
def answer() -> str:
    """
    Retorna uma resposta baseada na classificação de produtividade.

    Retorna a string representando o estado de produtividade.
    """
    # Placeholder para a lógica de resposta (implementar depois)
    return "Answer logic not implemented yet."
