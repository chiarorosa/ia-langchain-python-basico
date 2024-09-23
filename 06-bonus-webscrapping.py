import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import re
import random

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
    em_estoque TEXT,
    genero TEXT,
    avaliacao TEXT,
    descricao TEXT
)
''')

# Criando a tabela 'movimentacoes' se ainda não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER,
    quantidade INTEGER,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_movimentacao TEXT,
    FOREIGN KEY(livro_id) REFERENCES livros(id)
)
''')

# Função para salvar no banco de dados
def salvar_livro(livro):
    cursor.execute('''
    INSERT INTO livros (titulo, preco, em_estoque, genero, avaliacao, descricao)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (livro['titulo'], livro['preco'], livro['em_estoque'], livro['genero'], livro['avaliacao'], livro['descricao']))
    conn.commit()
    livro_id = cursor.lastrowid

    # Inserindo movimentação de entrada
    cursor.execute('''
    INSERT INTO movimentacoes (livro_id, quantidade, tipo_movimentacao)
    VALUES (?, ?, ?)
    ''', (livro_id, livro['quantitativo'], 'entrada'))
    conn.commit()

# Função para obter detalhes do livro
def obter_detalhes_do_livro(produto):
    try:
        livro_url = url_book.format(produto.select('a')[0]['href'])
        livro_page = requests.get(livro_url)
        soup_livro = BeautifulSoup(livro_page.text, 'lxml')

        titulo = soup_livro.select('.product_main h1')[0].text
        preco = soup_livro.select('.price_color')[0].text.split('£')[1]
        estoque_str = soup_livro.select('.instock.availability')[0].text.strip()
        avaliacao = soup_livro.select('.star-rating')[0]['class'][1]
        genero = soup_livro.select('.breadcrumb li')[2].text.strip()

        # Separando "Em estoque" e "Quantitativo"
        if 'In stock' in estoque_str:
            em_estoque = 'Sim'
            match = re.search(r'\((\d+) available\)', estoque_str)
            if match:
                quantitativo = int(match.group(1))
            else:
                quantitativo = 0
        else:
            em_estoque = 'Não'
            quantitativo = 0

        # Checando se a descrição existe
        descricao_elem = soup_livro.select('#product_description ~ p')
        if descricao_elem:
            descricao = descricao_elem[0].text
        else:
            descricao = 'Descrição não disponível'

        return {
            'titulo': titulo,
            'preco': float(preco),
            'em_estoque': em_estoque,
            'quantitativo': quantitativo,
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

print(f"Total de livros coletados e salvos: {len(livros)}")

# -----------------------------------------------------------------------
# Gerando saídas aleatórias para 100 livros
# -----------------------------------------------------------------------

# Obter todos os IDs de livros disponíveis
cursor.execute('SELECT id FROM livros')
livro_ids = [row[0] for row in cursor.fetchall()]

# Selecionar 100 IDs de livros aleatórios
livro_ids_selecionados = random.sample(livro_ids, 100)

for livro_id in livro_ids_selecionados:
    # Calcular o estoque atual do livro
    cursor.execute('''
    SELECT
        (SELECT COALESCE(SUM(quantidade), 0) FROM movimentacoes WHERE livro_id = ? AND tipo_movimentacao = 'entrada') -
        (SELECT COALESCE(SUM(quantidade), 0) FROM movimentacoes WHERE livro_id = ? AND tipo_movimentacao = 'saida')
    ''', (livro_id, livro_id))
    estoque_atual = cursor.fetchone()[0]

    if estoque_atual > 0:
        # Gerar uma quantidade de saída aleatória que não exceda o estoque atual
        quantidade_saida = random.randint(1, estoque_atual)

        # Inserir movimentação de saída
        cursor.execute('''
        INSERT INTO movimentacoes (livro_id, quantidade, tipo_movimentacao)
        VALUES (?, ?, ?)
        ''', (livro_id, quantidade_saida, 'saida'))
        conn.commit()
        print(f"Saída registrada para o livro ID {livro_id}: {quantidade_saida} unidades")
    else:
        print(f"O livro ID {livro_id} não possui estoque disponível para saída.")

# Fechar a conexão com o banco de dados
conn.close()
