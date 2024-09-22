import os
from decouple import config
from langchain_google_genai import GoogleGenerativeAI

'''
Este script usa a API do Google Generative AI através da biblioteca langchain_google_genai
para interagir com um modelo de linguagem grande (LLM). Ele faz uso da biblioteca python-decouple
para gerenciar a chave da API de forma segura.

Funcionalidades:
1. Usa o `python-decouple` para carregar a chave da API do Google Generative AI a partir de um arquivo `.env`.
2. Configura a chave da API como uma variável de ambiente.
3. Solicita ao usuário que faça uma pergunta, envia essa pergunta para o modelo Google Generative AI,
   e imprime a resposta gerada pelo modelo.

Requisitos:
- python-decouple: para carregar a chave da API do arquivo .env.
- langchain_google_genai: para usar o modelo Google Generative AI.

Como usar:
1. Certifique-se de que o arquivo `.env` contém a variável `API_KEY` com sua chave de API do Google Generative AI.
2. Execute o script e insira uma pergunta quando solicitado.

Exemplo do arquivo `.env`:
    API_KEY=google_api_key
'''

# Carregar chave da API do Google Generative AI do arquivo .env
os.environ['GOOGLE_API_KEY'] = config('API_KEY')

# Inicializar o modelo do Google Generative AI com o modelo especificado
modelo = GoogleGenerativeAI(model="gemini-1.5-flash") # neste caso versão gratuita da GoogleAI

# Solicitar uma pergunta ao usuário
pergunta = input('Me faça uma pergunta: ')

# Enviar a pergunta para o modelo e receber a resposta
resposta = modelo.invoke(pergunta)

# Exibir a resposta gerada
print(resposta)
