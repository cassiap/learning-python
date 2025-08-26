primeiro_valor = input ("Digite o primeiro valor: " )
segundo_valor = input ("Digite o segundo valor: " )
if primeiro_valor > segundo_valor:
    print (f"O maior valor é: {primeiro_valor}")
elif segundo_valor > primeiro_valor:
    print (f"O maior valor é: {segundo_valor}")
else:
    print ("Os valores são iguais")