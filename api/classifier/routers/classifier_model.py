from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from enum import Enum
from typing import Union

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
    
# DTo para Request
class MessageRequest(BaseModel):
    msg: str
    type: TypeDoc
