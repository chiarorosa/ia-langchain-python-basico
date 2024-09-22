import os
from decouple import config

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Carregar chave da API do Serper do arquivo .env
os.environ['SERPER_API_KEY'] = config('SERPER_API_KEY')

# Instanciando a classe DuckDuckGoSearchRun
duckduckgo = DuckDuckGoSearchRun()
# Instanciando a classe GoogleSerperAPIWrapper
serperdev = GoogleSerperAPIWrapper(gl="br", hl="pt-br")
# Instanciando a classe WikipediaQueryRun
wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        lang="pt",
    )
)

# Definindo a pesquisa
pesquisa = input('Digite o que deseja pesquisar: ')

# Realizando uma busca no DuckDuckGo
resultado = duckduckgo.run(pesquisa)
print("DuckDuckGo: "+resultado)

# Realizando uma busca no Serper
resultado = serperdev.run(pesquisa)
print("Serper: "+resultado)

resultado = wikipedia.run(pesquisa)
print("Wikipedia: "+resultado)
