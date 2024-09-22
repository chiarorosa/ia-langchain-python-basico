import os
from decouple import config

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Carregar chave da API do Google Generative AI do arquivo .env
os.environ['GOOGLE_API_KEY'] = config('API_KEY')

modelo = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash"
) # neste caso versão gratuita da GoogleAI

chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(
        content='Você é um assistente especializado em ajudar alunos que estão aprendendo os conceitos básicos de programação. Seu objetivo é responder de forma clara, amigável e didática, adaptando-se ao nível de entendimento de cada estudante'
    ),
    HumanMessagePromptTemplate.from_template(
        template='Acho que estou no nível {nivel} em programação'
    ),
    AIMessage(
        content='Certo, eu compreendo o seu nível de conhecimento em programação. Com o que você precisa de ajuda?'
    ),
    HumanMessagePromptTemplate.from_template(
        template='Minha dúvida é a seguinte: {pergunta}'
    ),
])

pergunta = input('Olá aluno, tire sua dúvida comigo: ')
nivel = input('Em que nível você se considera em programação? ')

prompt = chat_template.format_messages(
    nivel=nivel,
    pergunta=pergunta
)

print(prompt)

resposta = modelo.invoke(prompt)

print(resposta)
print(resposta.content)
