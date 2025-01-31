import os
import pdfplumber
from PyPDF2 import PdfReader
from fastapi import  APIRouter, UploadFile, File, HTTPException

from classifier.routers.classifier_model import TypeDoc, router, UploadFile, Union, MessageRequest
from classifier.routers.file_service import process_file
from classifier.routers.email_service import classify_email_groq, generate_response_groq, generate_response_gpt

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

# Rota para ler conteúdo de texto ou arquivo
@router.post("/read", response_model=str)
async def read(msg: Union[str, UploadFile], type: TypeDoc) -> str:
    """Lê e retorna o conteúdo do texto ou arquivo enviado."""
    if type == TypeDoc.STR:
        if isinstance(msg, str):
            return msg
        raise HTTPException(status_code=400, detail="Esperava-se uma string para o tipo STR.")

    if isinstance(msg, UploadFile):
        file_location = f"temp_{msg.filename}"
        with open(file_location, "wb") as temp_file:
            temp_file.write(await msg.read())
        
        content = process_file(file_location, type)
        os.remove(file_location)  # Remove o arquivo temporário
        return content

    raise HTTPException(status_code=400, detail="Tipo inválido fornecido.")

UPLOAD_DIR = "./tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/answer-mistral-docs")
async def answer_mistral(file: UploadFile = File(...)):
    """Processa um arquivo (TXT ou PDF), converte para string e classifica."""

    # Definir caminho para salvar o arquivo
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    # Salvar o arquivo recebido
    try:
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {e}")

    # Verificar se é um PDF válido
    if file.filename.endswith(".pdf") and not is_valid_pdf(file_location):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é um PDF válido.")

    # Verificar o tipo de arquivo e converter para string
    if file.filename.endswith(".txt"):
        content = txt_to_string(file_location)
    elif file.filename.endswith(".pdf"):
        content = pdf_to_string(file_location)
    else:
        raise HTTPException(status_code=400, detail="Formato não suportado. Envie um arquivo .txt ou .pdf")

    # Passar o conteúdo para o modelo Mistral-7B (função fictícia)
    result = generate_response_groq(content)

    return {
        "classification": result["classification"],
        "response": result["response"]
    }

# Rota para responder ao usuário usando Mistral-7B
@router.post("/answer-mistral")
async def answer_mistral(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo Mistral-7B."""
    
    result = generate_response_groq(request.msg)  # Obtém classificação e resposta

    return {
        "classification": result["classification"],
        "response": result["response"]
    }

# Rota para responder ao usuário usando gpt
@router.post("/answer-gpt")
async def answerGpt(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo gpt-3.5-turbo-0125 da OpenAI."""
    classification = classify_email_groq(request.msg)
    return generate_response_gpt(request.msg, classification)

