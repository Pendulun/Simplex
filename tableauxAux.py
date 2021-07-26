from tableaux import Tableaux
import numpy as np

class TableauxAux(Tableaux):

    def __init__(self, pl, cOriginal):
        super().__init__(pl)
        self.__cOriginalNegativado = cOriginal*-1