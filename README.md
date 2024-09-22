# LangChain + Python + LLM API

## Requisitos

- Python 3.x
- langchain
-

## Configuração do Ambiente Virtual

1. Verifique se o Python 3 está instalado:

   ```bash
   python3 --version
   ```

2. Crie o ambiente virtual:

   ```bash
   python3 -m venv venv
   ```

3. Ative o ambiente virtual:

   ```bash
   source venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install python-decouple
   pip install langchain
   pip install langchain-google-genai
   ```

## Uso do `python-decouple`

1. Crie um arquivo `.env` na raiz do projeto para armazenar suas variáveis sensíveis, como chaves de API:

   ```bash
   touch .env
   ```

2. No arquivo `.env`, adicione suas variáveis:

   ```env
   API_KEY=123456789abcdef
   ```

3. No seu código Python, use o `python-decouple` para acessar as variáveis:

   ```python
   from decouple import config

   api_key = config('API_KEY')
   print(f"Sua chave de API é: {api_key}")
   ```

## Executar o Projeto

1. Certifique-se de que o ambiente virtual está ativado:

   ```bash
   source venv/bin/activate
   ```

2. Execute seu script Python:

   ```bash
   python3 seu_script.py
   ```

## License

Este projeto é licenciado sob a [MIT License](LICENSE).
