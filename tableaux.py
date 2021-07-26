from maxPL import PL
import numpy as np

class Tableaux():
    def __init__(self, pl):
        self._valorOtimo = 0
        self.__certificadoOtimo = np.zeros(pl.numRestricoes())
        self.__matrizTransformacoes = np.identity(pl.numRestricoes())
        self.__cNegativo = pl.getC()*-1
        self.__matrizA = pl.getRestricoes()
        self.__vetorB = pl.getB()
    
    def print(self):
        print("{} | {} | {}".format(self.__certificadoOtimo, self.__cNegativo, self._valorOtimo))
        for i in range(self.numRestricoes()):
            print("{} | {} | {}".format(self.__matrizTransformacoes[i], self.__matrizA[i], self.__vetorB[i]))
    
    def numRestricoes(self):
        return self.__matrizA.shape[0]
    
    def getB(self):
        return self.__vetorB.copy()
    
    def getC(self):
        return self.__cNegativo.copy()
    
    def getMatrizA(self):
        return self.__matrizA.copy()
    
    def attValorB(self, numLinha, valor):
        self.__vetorB[numLinha] = valor
    
    def attLinhaA(self, numLinha, novaLinha):
        self.__matrizA[numLinha] = novaLinha
    
    def numVariaveisC(self):
        return self.__cNegativo.shape[0]
    
    def attValorC(self, numLinha, valor):
        self.__cNegativo[numLinha] = valor
    
    def getCertificadoOtimo(self):
        return self.__certificadoOtimo.copy()
    
    def getValorOtimo(self):
        return self._valorOtimo
    
    def getMatrizTransformacoes(self):
        return self.__matrizTransformacoes.copy()
    
    def attLinhaMatrizA(self, numLinha, novaLinha):
        self.__matrizA[numLinha] = novaLinha
    
    def attLinhaMatrizTransformacoes(self, numLinha, novaLinha):
        self.__matrizTransformacoes[numLinha] = novaLinha