import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# URL base para a paginação e para os livros
url_base = 'https://books.toscrape.com/catalogue/page-{}.html'
url_book = 'https://books.toscrape.com/catalogue/{}'

# Criando um banco de dados SQLite
conn = sqlite3.connect('livros.db')
cursor = conn.cursor()

# Criando a tabela 'livros' se ainda não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    preco REAL,
    estoque TEXT,
    genero TEXT,
    avaliacao TEXT,
    descricao TEXT
)
''')

# Função para salvar no banco de dados
def salvar_livro(livro):
    cursor.execute('''
    INSERT INTO livros (titulo, preco, estoque, genero, avaliacao, descricao)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (livro['titulo'], livro['preco'], livro['estoque'], livro['genero'], livro['avaliacao'], livro['descricao']))
    conn.commit()

# Função para obter detalhes do livro
def obter_detalhes_do_livro(produto):
    try:
        livro_url = url_book.format(produto.select('a')[0]['href'])
        livro_page = requests.get(livro_url)
        soup_livro = BeautifulSoup(livro_page.text, 'lxml')

        titulo = soup_livro.select('.product_main h1')[0].text
        preco = soup_livro.select('.price_color')[0].text.split('£')[1]
        estoque = soup_livro.select('.instock.availability')[0].text.strip()
        avaliacao = soup_livro.select('.star-rating')[0]['class'][1]
        genero = soup_livro.select('.breadcrumb li')[2].text.strip()

        # Checando se a descrição existe
        descricao = soup_livro.select('#product_description h2')
        if descricao:
            descricao = descricao[0].find_next('p').text
        else:
            descricao = 'Descrição não disponível'

        return {
            'titulo': titulo,
            'preco': float(preco),
            'estoque': estoque,
            'genero': genero,
            'avaliacao': avaliacao,
            'descricao': descricao
        }
    except Exception as e:
        print(f"Erro ao obter detalhes do livro: {e}")
        return None

# Loop para pegar todos os livros
livros = []
for i in range(1, 51):  # (ajuste conforme necessário)
    resultado = requests.get(url_base.format(i))
    soup = BeautifulSoup(resultado.text, 'lxml')
    produtos = soup.select('.product_pod')
    
    for produto in produtos:
        livro = obter_detalhes_do_livro(produto)
        if livro:
            livros.append(livro)
            salvar_livro(livro)
            print(f"Livro salvo: {livro['titulo']}")
        
        # Aguardar um tempo para evitar sobrecarregar o servidor
        time.sleep(0.3) # 300ms

# Fechar a conexão com o banco de dados
conn.close()

print(f"Total de livros coletados e salvos: {len(livros)}")
