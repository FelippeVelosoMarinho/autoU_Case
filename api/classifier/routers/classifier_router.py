from fastapi import  HTTPException, Form
import PyPDF2
import os
import requests
from dotenv import load_dotenv
from transformers import pipeline
from huggingface_hub import login

from classifier.routers.model import IsProductive, TypeDoc, router, UploadFile, Union, BaseModel

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
HF_API_KEY = os.getenv("MISTRAL_KEY")
GPT_MODEL = "gpt-3.5-turbo-0125"  # Modelo mais barato disponível
HF_MODEL_URL = "mistralai/Mistral-7B-Instruct-v0.3" # URL do modelo Mistral-7B

login(HF_API_KEY)

chatbot = pipeline("text-generation", model=HF_MODEL_URL, token=HF_API_KEY)


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
def generate_response_gpt(content: str, classification: IsProductive) -> str:
    prompt = f"O seguinte conteúdo foi classificado como {classification.name.lower()}:\n\n{content}\n\nGere uma resposta curta e objetiva explicando o motivo."

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
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

def generate_response_mistral(prompt: str, max_tokens: int = 100) -> str:
    messages = [
        {"role": "system", "content": "Você é um assistente de respostas automáticas para E-mails."},
        {"role": "user", "content": prompt}
    ]
    
    response = chatbot(messages, max_new_tokens=max_tokens)

    if isinstance(response, list) and len(response) > 0:
        return response[0]["generated_text"]  # Retorna o texto gerado
    return "Resposta não encontrada."

# Rota para responder ao usuário usando gpt
@router.post("/answer-gpt")
async def answerGpt(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo gpt-3.5-turbo-0125 da OpenAI."""
    classification = classify(request.msg)
    return generate_response_gpt(request.msg, classification)

# Rota para responder ao usuário usando Mistral-7B
@router.post("/answer-mistral")
async def answerMistral(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo Mistral-7B-v0.1 da Mistral AI."""
    classification = classify(request.msg)
    print(request.msg)
    return generate_response_mistral(request.msg)

