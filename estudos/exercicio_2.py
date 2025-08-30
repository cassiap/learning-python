'''
Exercicio
Peça ao usuário para digitar seu nome
Peça ao usuario para digitar sua idade
Se nome e idade forem digitados:
 Exiba:
 Seu nome é
 Seu nome invertido é
 Seu nome tem n letras
 A primeira letra do seu nome é
 A última letra do seu nome é
 Se nada for digitado em nome ou idade:
 Exiba "Desculpe, você deixou campos vazios."
'''
nome = input('Digite seu nome: ')
idade = input('Digite sua idade: ')

if nome and idade:
    print(f'Seu nome é {nome}')
    print(f'Seu nome invertido é {nome[::-1]}')
    print(f'Seu nome tem {len(nome)} letras')
    print(f'A primeira letra do seu nome é {nome[0]}')
    print(f'A última letra do seu nome é {nome[-1]}')
else:
    print('Desculpe, você deixou campos vazios.')