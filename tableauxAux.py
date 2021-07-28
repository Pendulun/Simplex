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
    
    def resultadoTornaPLOriginalViavel(self):
        return math.isclose(self._valorOtimo , 0, abs_tol=self.PRECISAO)
    
    def getCOriginalNegativado(self):
        return self._cOriginalNegativado.copy()
    
    def getValorOtimoDoCOriginal(self):
        return self._valorOtimoDoCOriginal
    
    def getCertificadoOtimoDoCOriginal(self):
        return self._certificadoOtimoDoCOriginal.copy()