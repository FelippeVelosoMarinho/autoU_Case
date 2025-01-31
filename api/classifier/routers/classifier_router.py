from fastapi import  HTTPException
import os

from classifier.routers.classifier_model import TypeDoc, router, UploadFile, Union, MessageRequest
from classifier.routers.file_service import process_file
from classifier.routers.email_service import classify_email_groq, generate_response_groq, generate_response_gpt

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

# Rota para responder ao usuário usando Mistral-7B
@router.post("/answer-mistral")
async def answer_mistral(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo Mistral-7B-v0.1 da Mistral AI."""
    classification = classify_email_groq(request.msg)  # Classifica a mensagem, como antes
    print(f"Mensagem classificada como {classification}")
    
    # Gerar resposta com o modelo Mistral
    response = generate_response_groq(request.msg)
    return {"response": response}

# Rota para responder ao usuário usando gpt
@router.post("/answer-gpt")
async def answerGpt(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo gpt-3.5-turbo-0125 da OpenAI."""
    classification = classify_email_groq(request.msg)
    return generate_response_gpt(request.msg, classification)

