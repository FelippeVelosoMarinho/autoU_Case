from fastapi import  HTTPException, Form
import PyPDF2
import os
import requests
from dotenv import load_dotenv
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer, TrainingArguments, Trainer
from huggingface_hub import login
from ctransformers import AutoModelForCausalLM

import pandas as pd
from datasets import Dataset

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from classifier.routers.model import IsProductive, TypeDoc, router, UploadFile, Union, BaseModel

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
HF_API_KEY = os.getenv("MISTRAL_KEY")
GPT_MODEL = "gpt-3.5-turbo-0125"  # Modelo mais barato disponível
#HF_MODEL_URL = "mistralai/Mistral-7B-Instruct-v0.3" # URL do modelo Mistral-7B
#HF_MODEL_URL = "./mistral_model" #os.path.abspath(os.path.join(os.path.dirname(__file__), "../../mistral_model"))

HF_MODEL_URL = os.path.abspath("./api/mistral_model")
print(f"Caminho absoluto do modelo: {HF_MODEL_URL}")

login(HF_API_KEY)

#chatbot = pipeline("text-generation", model=HF_MODEL_URL, token=HF_API_KEY)

#BERT Variables
# BERT_MODEL_NAME = "neuralmind/bert-base-portuguese-cased"
# tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)
# model = AutoModelForSequenceClassification.from_pretrained(BERT_MODEL_NAME, num_labels=2) # 2 labels = SPAM e Não-SPAM.

# # Carregar dataset (exemplo)
# df = pd.read_csv("emails.csv")

# # Remover linhas vazias
# df.dropna(inplace=True)

# # Converter para dataset do Hugging Face
# dataset = Dataset.from_pandas(df)

# # Dividir os dados
# train_test_split = dataset.train_test_split(test_size=0.2)
# train_dataset = train_test_split["train"]
# test_dataset = train_test_split["test"]

# # Configurações do treinamento
# training_args = TrainingArguments(
#     output_dir="./results",
#     evaluation_strategy="epoch",
#     save_strategy="epoch",
#     per_device_train_batch_size=8,
#     per_device_eval_batch_size=8,
#     num_train_epochs=3,
#     weight_decay=0.01,
#     logging_dir="./logs"
# )

# # Criar o Trainer
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=test_dataset
# )

# # Treinar o modelo
# trainer.train()

# # Fazer previsões no conjunto de teste
# predictions = trainer.predict(test_dataset)
# preds = predictions.predictions.argmax(axis=-1)

# # Calcular a acurácia
# accuracy = accuracy_score(test_dataset["label"], preds)
# print(f"Acurácia: {accuracy:.2f}")

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

##### USANDO BERT PARA CLASSIFICAÇÃO #######
# # O BERT exige que os textos sejam tokenizados antes do treinamento
# def tokenize_function(examples): 
#     return tokenizer(examples["texto"], truncation=True, padding="max_length", max_length=256)

# # Aplicar tokenização ao dataset
# tokenized_dataset = dataset.map(tokenize_function, batched=True)

# def classify_email(email_text):
#     inputs = tokenizer(email_text, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
#     outputs = model(**inputs)
#     prediction = outputs.logits.argmax().item()
#     return "SPAM" if prediction == 1 else "Não-SPAM"

#print(classify_email("Parabéns! Você ganhou um prêmio! Clique aqui para resgatar."))

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

# def generate_response_mistral(prompt: str, max_tokens: int = 100) -> str:
#     messages = [
#         {"role": "system", "content": "Você é um assistente de respostas automáticas para E-mails."},
#         {"role": "user", "content": prompt}
#     ]
    
#     response = chatbot(messages, max_new_tokens=max_tokens)

#     if isinstance(response, list) and len(response) > 0:
#         return response[0]["generated_text"]  # Retorna o texto gerado
#     return "Resposta não encontrada."

# Carregar o modelo .gguf
def load_mistral_model(model_path: str):
    try:
        model = AutoModelForCausalLM.from_pretrained(model_path)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar o modelo Mistral: {e}")

# Função para gerar resposta com o modelo Mistral
def generate_response_mistral(prompt: str, model, max_tokens: int = 100) -> str:
    try:
        # Gerar a resposta com o modelo .gguf usando o método de inferência
        response = model(prompt, max_new_tokens=max_tokens)

        # Se a resposta for uma string, retorne diretamente
        if isinstance(response, str):
            return response
        # Caso contrário, trata como um dicionário com a chave 'generated_text'
        elif isinstance(response, dict) and "generated_text" in response:
            return response["generated_text"]

        # Se nenhum dos casos se aplicar, levanta um erro
        raise HTTPException(status_code=500, detail="Formato inesperado na resposta do modelo.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resposta com o modelo Mistral: {e}")

# Inicialize o modelo fora das rotas para evitar carregar o modelo toda vez que a rota for chamada
mistral_model = load_mistral_model("./api/mistral-7b-instruct-v0.2.Q2_K.gguf")

# Rota para responder ao usuário usando Mistral-7B
@router.post("/answer-mistral")
async def answer_mistral(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo Mistral-7B-v0.1 da Mistral AI."""
    classification = classify(request.msg)  # Classifica a mensagem, como antes
    print(f"Mensagem classificada como {classification.name}")
    
    # Gerar resposta com o modelo Mistral
    response = generate_response_mistral(request.msg, mistral_model)
    return {"response": response}

# Rota para responder ao usuário usando gpt
@router.post("/answer-gpt")
async def answerGpt(request: MessageRequest):
    """Processa o conteúdo, classifica e gera uma resposta com o modelo gpt-3.5-turbo-0125 da OpenAI."""
    classification = classify(request.msg)
    return generate_response_gpt(request.msg, classification)

# # Rota para responder ao usuário usando Mistral-7B
# @router.post("/answer-mistral")
# async def answerMistral(request: MessageRequest):
#     """Processa o conteúdo, classifica e gera uma resposta com o modelo Mistral-7B-v0.1 da Mistral AI."""
#     classification = classify(request.msg)
#     print(request.msg)
#     return generate_response_mistral(request.msg)

