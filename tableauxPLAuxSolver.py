from tableauxSolver import TableauxSolver
from tableauxAux import TableauxAux
class TableauxPLAuxSolver(TableauxSolver):
    def __init__(self, pl, cOriginal):
        super().__init__(pl)
        self.__tableaux = TableauxAux(pl, cOriginal)
    
