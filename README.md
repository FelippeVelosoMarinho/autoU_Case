# autoU_Case - Documentação

Este repositório contém o código de um projeto que visa automatizar a classificação de emails e sugerir respostas automáticas com base no conteúdo dos emails recebidos. O sistema utiliza inteligência artificial para classificar os emails em categorias predefinidas: **Produtivo** e **Improdutivo**. A solução é composta por duas partes: um **cliente em React + Vite** e uma **API em FastAPI**.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

autoU_Case/ <br>
│<br>
├── client/               # Código do Cliente (React + Vite)<br>
├── api/                  # Código da API (FastAPI)<br>
└── README.md             # Documentação do projeto

- **client/**: Diretório contendo o código do cliente da aplicação, desenvolvido com **React** e **Vite**.
- **api/**: Diretório contendo a API da aplicação, construída com **FastAPI**.

## Como Rodar o Projeto

### Rodar Localmente

#### 1. **Rodando o Cliente (React + Vite)**

1. Navegue até o diretório do cliente:

   ```bash
   cd client
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

O cliente estará disponível em http://localhost:5173 por padrão.

#### 2. **Rodando a API (FastAPI)**
1. Navegue até o diretório da API:
   ```bash
   cd api
   ```
2. Instale as dependências (recomenda-se o uso de um ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o servidor da API:
   ```bash
   uvicorn main:app --reload
   ```

A API estará disponível em http://localhost:8001 por padrão.

#### 3. **Testes da API**
Para rodar os testes da API, use o seguinte comando no diretório da API:
   ```bash
   cd api
   python -m pytest
   ```
#### Rodando com Docker
Se preferir rodar o cliente e a API em containers Docker, siga as instruções abaixo.

### 1. Docker para o Cliente

1. Navegue até o diretório do cliente:
   ```bash
   cd client
   ```

2. Construa a imagem Docker e rode o container:
   ```bash
   docker compose up --build
   ```

O cliente estará disponível em http://localhost:5173 dentro do container Docker.

### 2. Docker para a API

1. Navegue até o diretório do cliente:
   ```bash
   cd api
   ```

2. Construa a imagem Docker e rode o container:
   ```bash
   docker compose up --build
   ```

A API estará disponível em http://localhost:8001 dentro do container Docker.

# Requisitos
## Para o Cliente
- Node.js (recomendado versão 16 ou superior)
- npm (gerenciador de pacotes do Node.js)
## Para a API
- Python 3.9 ou superior
- FastAPI
- Uvicorn
- pytest (para rodar testes)
## Dependências
### Para o Cliente (React + Vite)
- React
- Vite
- Outras dependências específicas do projeto (instaladas com npm install)
### Para a API (FastAPI)
- FastAPI
- Uvicorn
- Pydantic
- Outros pacotes para rodar a API (instalados com pip install)
## Objetivo do Projeto
Este projeto tem como objetivo a automação da leitura e classificação de emails recebidos. Ele visa identificar se um email é produtivo ou improdutivo, e também sugerir respostas automáticas baseadas na classificação do conteúdo do email.

### Categorias de Classificação de Email
- **Produtivo**: Emails que exigem uma ação ou resposta imediata, como solicitações de suporte, atualizações de status, dúvidas sobre sistemas ou processos.
- **Improdutivo**: Emails que não requerem uma ação imediata, como mensagens de felicitações, agradecimentos ou conteúdos irrelevantes.

# Referências

- [Case Prático AutoU - Estágio de Produtos Digitais AI](https://thunder-seatbelt-d29.notion.site/Case-Pr-tico-AutoU-Estagi-rio-de-Produtos-Digitais-AI-189e899741ea8017974ffc7a6ff92b1a)
- [PrimeReact FileUpload](https://primereact.org/fileupload/)
- [BERT - Hugging Face Transformers](https://huggingface.co/docs/transformers/model_doc/bert)
- [OpenAI SPAM Classifier](https://www.geeksforgeeks.org/spam-classification-using-openai/)
- [Email Spam Classification Dataset - Kaggle](https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv)
- [Spam Mails Dataset - Kaggle](https://www.kaggle.com/datasets/venky73/spam-mails-dataset/data)
- [Portuguese BERT - Hugging Face](https://huggingface.co/neuralmind/bert-base-portuguese-cased)
- [Mistral-7B-v0.3 - Hugging Face](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3)
