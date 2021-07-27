from maxPL import PL
import numpy as np

class Tableaux():
    def __init__(self, pl):
        self._valorOtimo = 0
        self._certificadoOtimo = np.zeros(pl.numRestricoes())
        self._matrizTransformacoes = np.identity(pl.numRestricoes())
        self._cNegativo = pl.getC()*-1
        self._matrizA = pl.getRestricoes()
        self._vetorB = pl.getB()
    
    def print(self):
        primeiraLinha = "{} | {} | {}".format(self._certificadoOtimo, self._cNegativo, self._valorOtimo)
        print(primeiraLinha)
        print("-"*len(primeiraLinha))
        for i in range(self.numRestricoes()):
            print("{} | {} | {}".format(self._matrizTransformacoes[i], self._matrizA[i], self._vetorB[i]))
    
    def numRestricoes(self):
        return self._matrizA.shape[0]
    
    def getB(self):
        return self._vetorB.copy()
    
    def getValorB(self, index):
        return self._vetorB[index]
    
    def getC(self):
        return self._cNegativo.copy()
    
    def getItemC(self, index):
        return self._cNegativo[index]
    
    def getMatrizA(self):
        return self._matrizA.copy()
    
    def getCopiaLinhaA(self, numLinha):
        return self._matrizA[numLinha]
    
    def attValorB(self, numLinha, valor):
        self._vetorB[numLinha] = valor
    
    def attLinhaA(self, numLinha, novaLinha):
        self._matrizA[numLinha] = novaLinha
    
    def numVariaveisC(self):
        return self._cNegativo.shape[0]
    
    def attValorC(self, numLinha, valor):
        self._cNegativo[numLinha] = valor
    
    def getCertificadoOtimo(self):
        return self._certificadoOtimo.copy()
    
    def getValorOtimo(self):
        return self._valorOtimo
    
    def getMatrizTransformacoes(self):
        return self._matrizTransformacoes.copy()
    
    def getCopiaLinhaMTransf(self, numLinha):
        return self._matrizTransformacoes[numLinha]
    
    def attLinhaMatrizA(self, numLinha, novaLinha):
        self._matrizA[numLinha] = novaLinha
    
    def attLinhaMatrizTransformacoes(self, numLinha, novaLinha):
        self._matrizTransformacoes[numLinha] = novaLinha
    
    def addMatrizA(self, submatriz):
        self._matrizA = np.hstack((self._matrizA, submatriz))
    
    def addNoCertificadoOtimo(self, linha):
        self._certificadoOtimo += linha
    
    def addNoVetorC(self, linha):
        self._cNegativo += linha
    
    def addNoValorOtimo(self, valor):
        self._valorOtimo += valor
    
    def addNoVetorB(self, index, valor):
        self._vetorB[index] += valor
    
    def addNaMatrizA(self, indexLinha, linha):
        self._matrizA[indexLinha] += linha
    
    def addNaMatrizTransf(self, indexLinha, linha):
        self._matrizTransformacoes[indexLinha] += linha