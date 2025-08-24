"""
DocString
Uma docstring (document string) é uma string de documentação usada para descrever o propósito e funcionamento de módulos, funções, classes ou métodos em Python.
Ela é colocada logo após a definição do elemento que será documentado, usando aspas triplas
Docstrings podem ser acessadas pelo atributo especial .__doc__ e são muito úteis para gerar documentação automática do código.
Python = Linguagem de programação
Tipo de tipagem = Dinâmica / Forte
str -> string -> texto
Strings são textos que estão dentro de aspas
"""
print(1234)

# Aspas simples
print('Luiz Otávio')
print(1, 'Luiz "Otávio"')

# Aspas duplas
print("Luiz Otávio")
print(2, "Luiz 'Otávio'")

# Escape
print("Luiz \"Otávio\"")

# r
print(r"Luiz \"Otávio\"")

''' diferença está no uso do prefixo r antes da string, que transforma a string em uma raw string (string bruta).

1. Sem o r (escape normal)
Aqui, o \" é interpretado como um caractere especial: uma aspa dupla dentro da string.
Saída: Luiz "Otávio"

2. Com o r (raw string)
Aqui, o prefixo r faz com que a barra invertida (\) seja tratada literalmente, não como caractere de escape.
Saída:Luiz \"Otávio\"

Resumo:

Sem r: o Python interpreta os escapes.
Com r: o Python mostra a barra invertida como está no texto.
Isso é útil, por exemplo, para caminhos de arquivos no Windows ou expressões regulares.'''