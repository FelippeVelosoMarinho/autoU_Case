import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests

from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router
from classifier.routers import classifier_router

load_dotenv()
app = FastAPI()

api_key = os.getenv("API_KEY")

# criar requisição
headers = {"Authorization":  f"Bearer {api_key}"}
link = "https://api.openai.com/v1/models"
requisicao = requests.get(link, headers=headers)

@app.get("/")
def hello() -> str:
        print(requisicao)
        print(requisicao.text)
        return "OIIII"
    
app.include_router(contas_a_pagar_e_receber_router.router)
app.include_router(classifier_router.router)

if __name__  == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)