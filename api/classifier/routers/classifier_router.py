import os
from PyPDF2 import PdfReader
from fastapi import  UploadFile, File, HTTPException

from classifier.routers.classifier_model import TypeDoc, router, UploadFile, MessageRequest
from classifier.routers.file_service import txt_to_string, pdf_to_string, is_valid_pdf
from classifier.routers.email_service import classify_email_groq, generate_response_groq

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
