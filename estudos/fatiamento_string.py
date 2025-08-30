'''
Fatiamento de strings
012345678
Olá mundo
-987654321
Fatiamento [i:f:p] [::]
Obs.: a função len retorna o tamanho da string
'''
variavel = 'Olá mundo'
print(variavel[0:5] )  # Olá m

print(len(variavel))

print(variavel[0:9:3])

print(variavel[::-1])  # Invertendo a string