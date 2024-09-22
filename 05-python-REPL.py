from langchain_experimental.utilities import PythonREPL

'''
Este script utiliza o `PythonREPL` da biblioteca `langchain_experimental.utilities` para executar
código Python dinamicamente em um ambiente de interpretação dentro do próprio script.
'''
repl = PythonREPL()
resultado = repl.run("print('Olá, 42!')")

print(resultado)
