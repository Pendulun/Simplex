import math
from tableaux import Tableaux
import numpy as np
import math
from maxPL import PL

class TableauxAux(Tableaux):
    PRECISAO=0.0001

    def __init__(self):
        super(TableauxAux, self).__init__()
    
    def setPLECOriginal(self, pl, cOriginal):
        self.setPL(pl)
        self._cOriginalNegativado = cOriginal*-1
        vetorZerosArtificiais = np.zeros(self.numRestricoes())
        self._cOriginalNegativado = np.concatenate((self._cOriginalNegativado,vetorZerosArtificiais), axis=None)
        self._valorOtimoDoCOriginal = 0
        self._certificadoOtimoDoCOriginal = np.zeros(pl.numRestricoes())
    
    def setTableauxECOriginal(self,tableaux,cOriginal):
        self.copiaDoTableaux(tableaux)
        self._cOriginalNegativado = cOriginal*-1
        vetorZerosArtificiais = np.zeros(self.numRestricoes())
        self._cOriginalNegativado = np.concatenate((self._cOriginalNegativado,vetorZerosArtificiais), axis=None)
        self._valorOtimoDoCOriginal = 0
        self._certificadoOtimoDoCOriginal = np.zeros(tableaux.numRestricoes())
    
    def print(self):
        self._imprimeLinhaC()
        self._imprimeLinhasMatrizTranfAB()
        self._imprimeLinhaCOriginal()

    def _imprimeLinhaCOriginal(self):
        print("C ORIGINAL:")
        primeiraLinha = "{} | {} | {}".format(self._certificadoOtimoDoCOriginal,
         self._cOriginalNegativado, self._valorOtimoDoCOriginal)
        print(primeiraLinha)
        print("-"*len(primeiraLinha))
    
    def resultadoTornaPLOriginalViavel(self):
        return math.isclose(self._valorOtimo , 0, abs_tol=self.PRECISAO)
    
    def getCOriginalNegativado(self):
        return self._cOriginalNegativado.copy()
    
    def getValorOtimoDoCOriginal(self):
        return self._valorOtimoDoCOriginal
    
    def getCertificadoOtimoDoCOriginal(self):
        return self._certificadoOtimoDoCOriginal.copy()
    
    def getElementoCOriginal(self, index):
        return self._cOriginalNegativado[index]
    
    def attValorCOriginal(self, index, valor):
        self._cOriginalNegativado[index] = valor
    
    def addNoCertificadoOtimoOriginal(self, linha):
        self._certificadoOtimoDoCOriginal += linha
    
    def addNoVetorCOriginal(self, linha):
        self._cOriginalNegativado += linha
    
    def addNoValorOtimoOriginal(self, valor):
        self._valorOtimoDoCOriginal += valor