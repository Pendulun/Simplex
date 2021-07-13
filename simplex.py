import numpy as np

class Simplex():
    """
    Essa classe tem o objetivo de ser um Solver para PL's no seguinte formato:
    max c_T*X
    sujeito a AX <= b e X>=0
    aplicando  o algoritmo Simplex
    """
    def __init__(self,n,m,c,b,restricoes):
        self.n = n
        self.m = m
        self.c = c
        self.b = b
        self.restricoes = restricoes
        pass

    def resolver(self):
        self.imprimeTudo()

    def imprimeTudo(self):
        print("Número de restrições: {}".format(self.n))
        print("Número de variáveis: {}".format(self.m))
        print("Vetor C: {}".format(self.c))
        print("Vetor B: {}".format(self.b))
        print("Restrições: {}".format(self.restricoes))

    def trocaSinalRestricaoSeBNaoPositivo(self,b,restricoes):
        print("TROCA SINAL")
        for i in range(b.size):
            if b[i]<0:
                restricoes[i] = restricoes[i] * -1
                b[i] = b[i] * -1