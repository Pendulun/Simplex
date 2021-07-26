from tableauxSolver import TableauxSolver
from tableauxAux import TableauxAux
import math
import numpy as np

class TableauxPLAuxSolver(TableauxSolver):

    PRECISAO = 0.0001

    def __init__(self, pl, cOriginal):
        super().__init__(pl)
        self._tableaux = TableauxAux(pl, cOriginal)
    
    def getTableaux(self):
        return self._tableaux

    def resolver(self):
        #Tratar B negativos
        self._trataBNegativoPL()

        #Adicionar Variáveis artificiais em A
        self._adicionarVariaveisArtificiais()

        #resolve

        #retorna o tableaux em sua forma final
        return self._tableaux

    def _trataBNegativoPL(self):
        print("TRATANDO B_i's negativos")
        b = self._tableaux.getB()
        restricoes = self._tableaux.getMatrizA()
        tranformacoes = self._tableaux.getMatrizTransformacoes()
        for i in range(self._tableaux.numRestricoes()):
            if math.isclose(b[i], 0, abs_tol=self.PRECISAO):
                #Define como 0.0, já que é perto mesmo
                self._tableaux.attValorB(i, 0.0)
            elif b[i] < 0:
                # Multiplica b[i], restricoes[i] e tranformacoes[i] por -1
                self._tableaux.attValorB(i,b[i]*-1)
                self._tableaux.attLinhaA(i,restricoes[i]*-1)
                self._tableaux.attLinhaMatrizTransformacoes(i,tranformacoes[i]*-1)
        self._tableaux.print()
    
    def _adicionarVariaveisArtificiais(self):
        print("ADICIONANDO VARIAVEIS ARTIFICIAIS MATRIZ A")
        variaveisArt = self.__geraMatrizIdentidade(self._tableaux.numRestricoes())
        self._tableaux.addMatrizA(variaveisArt)
        self._tableaux.print()
    
    def __geraMatrizIdentidade(self, tam):
        print("Gera Matriz Identidade")
        return np.identity(tam)

    
