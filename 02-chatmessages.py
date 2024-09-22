import os
from decouple import config

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Carregar chave da API do Google Generative AI do arquivo .env
os.environ['GOOGLE_API_KEY'] = config('API_KEY')

modelo = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash"
) # neste caso versão gratuita da GoogleAI

pergunta = input('Olá aluno, tire sua dúvida comigo: ')

mensagens = [
    SystemMessage(content='Você é um assistente especializado em ajudar alunos que estão aprendendo os conceitos básicos de programação. Seu objetivo é responder de forma clara, amigável e didática, adaptando-se ao nível de entendimento de cada estudante. Sempre que possível, forneça exemplos simples e evite jargões técnicos complexos, a menos que seja necessário explicá-los de maneira acessível. Se o aluno fizer uma pergunta muito ampla, ajude-o a focar no problema específico. Encorage o raciocínio lógico e incentive a prática, oferecendo dicas e sugestões úteis. Lembre-se de que os alunos estão no começo da jornada e podem precisar de paciência e explicações detalhadas. Seu foco está em linguagens como Python, JavaScript e lógica de programação, mas você pode ajudar em outros tópicos básicos também, como estruturas de dados simples e controle de fluxo.'),
    HumanMessage(content='Eu sou um bem iniciante em programação'),
    AIMessage(content='Olá! Como posso te ajudar?'),
    HumanMessage(content=pergunta)
]

resposta = modelo.invoke(mensagens)

print(resposta)
print(resposta.content)
