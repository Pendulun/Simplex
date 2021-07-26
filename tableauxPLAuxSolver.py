from tableauxSolver import TableauxSolver
from tableauxAux import TableauxAux
import math

class TableauxPLAuxSolver(TableauxSolver):

    PRECISAO = 0.0001

    def __init__(self, pl, cOriginal):
        super().__init__(pl)
        self.__tableaux = TableauxAux(pl, cOriginal)
    
    def getTableaux(self):
        return self.__tableaux

    
