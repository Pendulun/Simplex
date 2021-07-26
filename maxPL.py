import numpy as np

class PL():

    def __init__(self,c,b,restricoes):
        self.__c = c
        self.__b = b
        self.__restricoes = restricoes
    
    def copia(self):
        return PL(self.getC(), self.getB(), self.getRestricoes())

    def numRestricoes(self):
        return self.__restricoes.shape[0]
    
    def numVariaveisRestricoes(self):
        return self.__restricoes.shape[1]
    
    def numVariaveisC(self):
        return self.__c.shape[0]
    
    def getDiferencaNumVariaveisCERestricoes(self):
        return self.__c.shape[0] - self.__restricoes.shape[1]
    
    def print(self):
        print("C: {}".format(self.__c))
        print("B: {}".format(self.__b))
        print("Restrições:\n {}".format(self.__restricoes))
    
    def getRestricoes(self):
        return self.__restricoes.copy()
    
    def setRestricoes(self,novasRestricoes):
        self.__restricoes = novasRestricoes

    def getC(self):
        return self.__c.copy()
    
    def setC(self, novoC):
        self.__c = novoC

    def getB(self):
        return self.__b.copy()
    
    def setB(self, novoB):
        self.__b = novoB
    
    def attValorB(self, numLinha, valor):
        self.__b[numLinha] = valor
    
    def attLinhaRestricoes(self, numLinha, novaLinha):
        self.__restricoes[numLinha] = novaLinha
    
    def addEmC(self, vetor):
        self.__c = np.concatenate((self.__c,vetor), axis=None)