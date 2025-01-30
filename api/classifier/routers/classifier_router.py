from fastapi import  HTTPException, Form
import PyPDF2
import os
import requests
from dotenv import load_dotenv

from classifier.routers.model import IsProductive, TypeDoc, router, UploadFile, Union, BaseModel

load_dotenv()
API_KEY = os.getenv("API_KEY")
GPT_MODEL = "gpt-3.5-turbo-0125"  # Modelo mais barato disponível

# Definição do modelo para aceitar JSON
class MessageRequest(BaseModel):
    msg: str
    type: TypeDoc

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

# Função de classificação
def classify(msg: str) -> IsProductive:
    return IsProductive.PRODUCTIVE if len(msg.strip()) > 50 else IsProductive.IMPRODUCTIVE

# Função para gerar resposta via OpenAI
def generate_response(content: str, classification: IsProductive) -> str:
    prompt = f"O seguinte conteúdo foi classificado como {classification.name.lower()}:\n\n{content}\n\nGere uma resposta curta e objetiva explicando o motivo."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GPT_MODEL,
        "messages": [
            {"role": "system", "content": "Você é um assistente de análise de produtividade."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 30
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    # Mostra a resposta da OpenAI para entender o erro
    raise HTTPException(status_code=response.status_code, detail=f"Erro OpenAI: {response.text}")


# Rota principal para responder ao usuário
@router.post("/answer")
async def answer(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com IA."""
    classification = classify(request.msg)
    return generate_response(request.msg, classification)
# @router.post("/answer")
# async def answer(
#     msg: Union[str, UploadFile] = Form(...),
#     type: TypeDoc = Form(...)
# ):
#     # Verifica se é um arquivo
#     if isinstance(msg, UploadFile):
#         content = await msg.read()
#         content = content.decode("utf-8")  # Converte bytes para string
#     else:
#         content = msg

#     classification = classify(content)
#     return generate_response(content, classification)
