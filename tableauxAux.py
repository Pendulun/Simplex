import math
from tableaux import Tableaux
import numpy as np
import math

class TableauxAux(Tableaux):
    PRECISAO=0.0001

    def __init__(self, pl, cOriginal):
        super(TableauxAux, self).__init__(pl)
        self._cOriginalNegativado = cOriginal*-1
    
    def resultadoTornaPLOriginalViavel(self):
        return math.isclose(self._valorOtimo , 0, abs_tol=self.PRECISAO)