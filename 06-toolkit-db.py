import os
from decouple import config

from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

'''
InfoSQLDatabaseTool,
ListSQLDatabaseTool,
QuerySQLCheckerTool,
QuerySQLDataBaseTool,
'''

# Carregar chave da API do Google Generative AI do arquivo .env
os.environ['GOOGLE_API_KEY'] = config('API_KEY')

modelo = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash"
) # neste caso versão gratuita da GoogleAI

# Criar um banco de dados SQLite
db = SQLDatabase.from_uri('sqlite:///livros.db') # conexão com banco de dados relacional

# Criar um toolkit para manipular o banco de dados
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=modelo
)

# Langchain Hub [https://smith.langchain.com/hub]
system_message = hub.pull('hwchase17/react')
print(system_message)

# Criar um agente de reação
agente = create_react_agent(
    llm=modelo,
    tools=toolkit.get_tools(),
    prompt=system_message
)

# Executar o agente
executor = AgentExecutor(
    agent=agente,
    tools=toolkit.get_tools(),
    verbose=True
)

prompt = '''
Traduza a pergunta para Inglês antes de tudo. Utilize as ferramentas adequadas para responder, de forma detalhada e clara, às perguntas relacionadas aos livros do e-commerce para o qual você presta consultoria. Todas as respostas devem ser fornecidas em português do Brasil. Pergunta: {query}
'''

prompt_template = PromptTemplate.from_template(prompt)

pergunta = input('Olá, sou um consultor virtual de sua loja de livros. Como posso ajudar você hoje? ')

resultado = executor.invoke({
    'input': prompt_template.format(query=pergunta),
})

print(resultado.get('output'))

## Faça a pergunta: "Qual é o livro mais bem avaliado e caro da loja?"
## Faça a pergunta: "Tenho algum livro cadastrado em duplicidade no sistema?"