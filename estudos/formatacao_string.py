# d - int
# f - float
#.<numero de digitos>f - quantidade de casas decimais
# x e X - Hexadecimal (ABCDEF0123456789)
#(Caractere)(><^)(quantidade)
#> - esquerda
#< - direita
#^ - centro
#sinal - + ou -
#= - o sinal fica junto com o número
# Ex: 0>-100,.1f
#conversion flags - !r !s !a __repr__ __str__ __ascii__

variavel = 'ABC'
print(f'{variavel}')
print(f'{variavel: >10}')
print(f'{variavel: <10}')
print(f'{variavel: ^10}')
print(f'{1000.48756465:0=+10.1f}')
print(f'O hexadecimal de 1500 é {1500:08X}')
