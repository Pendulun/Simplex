import numpy as np
from tableaux import Tableux

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
        if(self.__verificaViabilidade()):
            self.__completarVariaveisFolga()
            self.imprimeTudo()
            self.__trocaSinalLinhaSeBNaoPositivo()
            self.imprimeTudo()
        else:
            pass
        

    def __verificaViabilidade(self):
        plAux = self.__geraPLAuxiliar()
        my_tableux = Tableux(self.c,self.b,self.restricoes)
        my_tableux.resolver()
        my_tableux.imprimirTudo()
        if(my_tableux.getValorOtimo() < 0):
            return False
        elif(my_tableux.getValorOtimo() > 0):
            print("Algo deu errado! Valor ótimo da PL Auxiliar é maior que 0!")
        else:
            return True

    def __geraPLAuxiliar(self):
        pass

    def imprimeTudo(self):
        print("Número de restrições: {}".format(self.n))
        print("Número de variáveis: {}".format(self.m))
        print("Vetor C: {}".format(self.c))
        print("Vetor B: {}".format(self.b))
        print("Restrições: {}".format(self.restricoes))

    def __trocaSinalLinhaSeBNaoPositivo(self):
        print("TROCA SINAL")
        for i in range(self.b.size):
            if self.b[i]<0:
                self.restricoes[i] = self.restricoes[i] * -1
                self.b[i] = self.b[i] * -1
    
    def __completarVariaveisFolga(self):
        print("Completar variáveis de Folga")
        identidade = np.identity(self.n)
        print("identidade: {}".format(identidade))
        self.restricoes = np.hstack((self.restricoes,identidade))