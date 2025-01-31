import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

from classifier.routers.classifier_model import IsProductive

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "mixtral-8x7b-32768"
OPENAI_KEY = os.getenv("OPENAI_KEY")
GPT_MODEL = "gpt-3.5-turbo-0125"

def classify_email_groq(email_text: str) -> str:
    """Classifica um email como PRODUTIVO ou IMPRODUTIVO usando a API da Groq."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Definir um prompt claro para classificar emails
    prompt = f"""
    Você é um assistente especializado em classificar emails como produtivos ou improdutivos. 
    - Um email **produtivo** contém informações úteis, como atualizações de trabalho, reuniões ou tarefas importantes. 
    - Um email **improdutivo** contém spam, promoções irrelevantes ou conteúdo que não agrega valor ao trabalho.

    Classifique o seguinte email apenas com 'PRODUTIVO' ou 'IMPRODUTIVO':

    ---
    {email_text}
    ---
    
    Responda apenas com 'PRODUTIVO' ou 'IMPRODUTIVO', sem explicações adicionais.
    """

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are an assistant for answering e-mails."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 10
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()

    raise HTTPException(status_code=response.status_code, detail=f"Erro na API da Groq: {response.text}")


def generate_response_groq(email_text: str, max_tokens: int = 100) -> dict:
    """Classifica o e-mail e gera uma resposta usando a API da Groq."""
    # Primeiro, classifica o e-mail
    classification = classify_email_groq(email_text)

    # Agora, gera a resposta
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"O seguinte e-mail foi classificado como {classification.lower()}:\n\n{email_text}\n\nGere uma resposta curta e objetiva."

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are an assistant for answering e-mails."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        generated_text = response.json()["choices"][0]["message"]["content"]
        return {
            "classification": classification,
            "response": generated_text
        }

    raise HTTPException(status_code=response.status_code, detail=f"Erro na API da Groq: {response.text}")

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
            {"role": "system", "content": "You are an assistant for answering e-mails."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 30
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    # Mostra a resposta da OpenAI para entender o erro
    raise HTTPException(status_code=response.status_code, detail=f"Erro OpenAI: {response.text}")
