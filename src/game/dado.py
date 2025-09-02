import random

class Dado:
    def __init__(self):
        self.dado1 = 0
        self.dado2 = 0
        self.resultados = []

    def tirar(self):
        resultado1 = self.dado1.tirar()
        resultado2 = self.dado2.tirar()
        
        if resultado1 == resultado2:
            self.resultados = [resultado1] * 4
        else:
            self.resultados = [resultado1, resultado2]