##################################
# Pedro Henrique Silva Domingues #
# R.A.: 11.115.253-4             #
##################################

import numpy as np
from random import randrange
from datetime import date, timedelta

def __ex1():
    done = False
    while not done:
        try:
            # input do usuario
            dias = int(input("dias > "))
            data = input("horas:min:seg > ").split(":")
            # convertendo dados de string para inteiro
            horas, minutos, seg = [int(i) for i in data]
            done = True
        except ValueError:
            print("formatacao incorreta ou entrada invalida")
    # calculo do tempo em segundos
    tempo_s = dias*86400 + horas*3600 + minutos*60 + seg
    # resposta do sistema
    print("tempo em segundos: {}".format(tempo_s))
    return

# ======================================================= #

def __ex2():
    done = False
    while not done:
        # input do usuario
        numeros = input("Digite os números: ").split(" ")
        try:
            # converte numeros para inteiro e ignora espaços
            numeros = [int(i) for i in numeros if i]
            if len(numeros) > 1: done = True
            else: print("Erro: Digite pelomenos dois numeros")
        except ValueError:
            print("Insira apenas numeros")

    print("O maior número é: ", end='')
    # compara e encontra o maior dos dois valores
    maior = numeros[0]
    for val in numeros:
        maior = val if val > maior else maior
    print(maior)
    return

# ======================================================= #

def __ex3():
    done = False
    while not done:
        try:
            # input do usuario
            salario = float(input("Salario: R$"))
            done = True
        except ValueError:
            print("Erro: valor inserido invalido...")

    aumento = 0.1 if salario > 1250 else 0.15
    print("Aumento de {}%, novo salario = R${:.2f}".format(aumento*100, salario*(1+aumento)))
    return

# ======================================================= #

def __ex4():
    # objeto combustivel armazena qualquer tipo de combustivel
    class Combustivel:
        def __init__(self, preco_litro, descontos, litros_desconto=20):
            #   preco_litro = preço de 1 litro do combustivel correspondente
            #   descontos = lista com os descontos referentes a <= e > que o ponto de corte
            #   litros_desconto = ponto de corte para trocar o valor do desconto (padrao 20)

            self.preco = preco_litro
            self.descontos = descontos
            self.litros_desconto = litros_desconto

        def desconto(self, litros):
            _desconto = self.descontos[0] if litros <= self.litros_desconto else self.descontos[1]
            a_pagar = litros*self.preco*(1-_desconto)
            return (a_pagar, _desconto)

    # Dicionario de combustiveis, para facil maior escalabilidade
    tabela_precos = {
        "alcool"    : Combustivel(3.19, [0.03, 0.05]),
        "gasolina"  : Combustivel(4.59, [0.04, 0.06])
    }

    done = False
    while not done:
        # entrada de dados
        combustivel = input("alcool ou gasolina? ").lower()
        try:
            litros = float(input("Qtd. em litros vendido: "))
            done = True
        except ValueError:
            print ("Erro: valor invalido...")
            done = False
            continue

        # calculando a resposta para o usuario
        try:
            a_pagar, desconto = tabela_precos[combustivel].desconto(litros)
            done = True
        except KeyError:
            print("combustivel invalido")
            done = False

    print("Desconto de {}% por litro, valor a ser pago: R${:.2f}".format(desconto*100, a_pagar))
    return

# ======================================================= #

def __ex5():
    # variaveis auxiliares
    numbers = []
    zero = False

    while not zero:
        data = input("Numeros >>> ").split(" ")
        try:
            data = [float(i) for i in data if i] # converte os numeros para float
        except ValueError:
            print ("Erro, use apenas numeros...")
            return
        if 0 in data:
            data = data[:data.index(0)]
            zero = True # se encontrar um 0 nos numeros digitados para
        numbers += data # concatena data aos numeros digitados

    print("Valores contabilizados: ", numbers)
    print("\t- Quantidade de numeros: {} \n\t- Soma: {}\n\t- Media aritmetica: {}".format(
        len(numbers), sum(numbers), np.mean(numbers)
    ))
    return
# ======================================================= #

def __ex6():
    numbers = []
    qtd = 20
    while qtd > 0:
        data = input("Numeros >>> ").split(" ")
        try:
            data = [int(i) for i in data if i] # converte os numeros para float
            if len(data) > qtd: data = data[:qtd]
            qtd -= len(data)
            numbers += data # concatena data aos numeros digitados
        except ValueError:
            print ("Erro, use apenas numeros...")

    par = [i for i in numbers if i%2==0]
    impar = [i for i in numbers if i%2==1]

    print("lista: ", numbers)
    print("pares: ", par)
    print("impares: ", impar)
    return

# ======================================================= #

def __ex7():
    i = 0
    loteria = []
    while i < 6:
        number = randrange(1,50)
        if number not in loteria:
            loteria.append(number)
            i += 1
    print("loteria: ", loteria)
    return

# ======================================================= #

def __ex8():
    print("Datas magicas entre 01/01/1901 ate hoje: ")
    input("Pressione qualquer tecla para visualizar as datas")
    # Para mecher com datas usarei a biblioteca datetime.
    # Mais especificamente a classe date para controle da data
    # e a função timedelta que gerencia a classe data para ir
    # dias para frente ou para tras.
    iterator = date(1901,1,1) # partindo de 01/01/1901
    end = date.today() # ate hoje
    while iterator != end:
        day = iterator.day
        month = iterator.month
        year = iterator.year % 100 # %100 para pegar o resto da divisao por 100 (ultimos dois digitos)
        if day*month == year: print("{}/{}/{}".format(day, month, iterator.year))
        iterator += timedelta(1)
    return

# ======================================================= #

def __ex9():
    class Retangulo:
        def __init__(self, lado1, lado2):
            self.lado1 = lado1
            self.lado2 = lado2
        def area(self): return self.lado1*self.lado2
        def perimetro(self): return 2*self.lado1 + 2*self.lado2
        def get_lado(self): return (self.lado1, self.lado2)
        def set_lado(self, novo1, novo2):
            self.lado1 = novo1
            self.lado2 = novo2

    # criando uma funcao para input dos lados
    def lados_user():
        # puxa 2 valores do usuario e confere se sao validos
        done = False
        while not done:
            try:
                lados = [int(input("lado {}: ".format(i))) for i in range(1,3)]
                done = True
            except ValueError:
                print("lado invalido...")
        return (lados[0], lados[1])

    # um dicionario que guarda os retangulos com seus respectivos nomes
    retangulos = {}
    for i in range(1,3):
        print("-> ret{}".format(i))
        lado1, lado2 = lados_user()
        retangulos["ret{}".format(i)] = Retangulo(lado1, lado2)
        print("-"*30)

    # varre os retangulos criados exibindo os detalhes
    for key in retangulos:
        print(key + ":")
        print("\t- Lados: ", retangulos[key].get_lado())
        print("\t- Area: ", retangulos[key].area())
        print("\t- Perimetro: ", retangulos[key].perimetro())
        print("-"*30)

    return

# ======================================================= #

# Rodando os exercicios
exercicios = [__ex1, __ex2, __ex3, __ex4, __ex5, __ex6, __ex7, __ex8, __ex9]
for idx, ex in enumerate(exercicios):
    print("="*50)
    print(">>> Exercicio {} <<<\n".format(idx+1))
    ex()
