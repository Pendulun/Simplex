from tableaux import Tableaux
from tableauxSolver import TableauxSolver
from tableauxAux import TableauxAux
import math
import numpy as np

class TableauxPLAuxSolver(TableauxSolver):

    PRECISAO = 0.0001

    def __init__(self, pl, cOriginal):
        super().__init__()
        self.comBaseNaPl(pl)
        self._tableaux = TableauxAux()
        self._tableaux.setPLECOriginal(pl, cOriginal)
    
    def getTableaux(self):
        return self._tableaux

    def resolver(self):
        #Tratar B negativos multiplicando-os por -1 sem fazer nenhum pivoteamento
        self._verificarB()

        #Adicionar Variáveis artificiais em A
        self._adicionarVariaveisArtificiaisEmA()

        #zerar todas as entradas em C relacionadas às variáveis artificiais
        self._zerarVariaveisArtificiaisDeC()
        print("TABLEAUX DEPOIS DE ZERAR EM C VAR ARTIFICIAIS")
        self._tableaux.print()

        #para todo C_i negativo, pivotear
        #definido em super
        self._trataCNegativo()

        #retorna o tableaux em sua forma final
        return self._tableaux
    
    def  _verificarB(self):
         while True:
            indexBINegativo = self._getIndexBINegativo()
            if indexBINegativo < 0:
                break
            else:
                print("INDEX B NEGATIVO: {}".format(indexBINegativo))
                self._trataBiNegativo(indexBINegativo)

    def _getIndexBINegativo(self):
        b = self._tableaux.getB()
        for i in range(self._tableaux.numRestricoes()):
            if math.isclose(b[i], 0, abs_tol=self.PRECISAO):
                #Define como 0.0, já que é perto mesmo
                self._tableaux.attValorB(i, 0.0)
            elif b[i] < 0:
                return i
        return -1

    def _trataBiNegativo(self, index):
        self._multiplicaLinhaPor(index+1,-1)
        self._tableaux.print()
    
    def _adicionarVariaveisArtificiaisEmA(self):
        print("ADICIONANDO VARIAVEIS ARTIFICIAIS MATRIZ A")
        variaveisArt = self.__geraMatrizIdentidade(self._tableaux.numRestricoes())
        self._tableaux.addMatrizA(variaveisArt)
        self._tableaux.print()
    
    def __geraMatrizIdentidade(self, tam):
        print("Gera Matriz Identidade")
        return np.identity(tam)

    def _zerarVariaveisArtificiaisDeC(self):
        indexPrimeiraColDeCVarArtificiais = self._tableaux.numVariaveisC() - self._tableaux.numRestricoes()
        print("INDEX PRIMEIRA COLUNA ARITIFICIAL EM C {}".format(indexPrimeiraColDeCVarArtificiais))
        print("NUMERO DE RESTRICOES: {}".format(self._tableaux.numRestricoes()))
        #Para cada linha de A, somar no vetor C
        for indexLinhaMatrizA in range(self._tableaux.numRestricoes()):
            #Já que já sei que no vetor i de A tem um elemento igual a 1
            self._adicionaLinhaMatrizANaLinhaAlvoTableauxNumVezes(indexLinhaMatrizA, 0,  -1)
            print("ADICIONANDO LINHA {} DE A EM C".format(indexLinhaMatrizA))
            self._tableaux.print()
    
    def get_tableaux_segunda_parte(self):
        print("TABLEAUX ATUAL A IR PARA A SEGUNDA PARTE")
        self._tableaux.print()
        tableaux_segunda_parte_simplex = Tableaux()
        tableaux_segunda_parte_simplex.copiaDoTableaux(self._tableaux)
        #remove as colunas das variáveis artificiais de c e de A
        novoC = self._tableaux.getCOriginalNegativado()
        novoA = self._tableaux.getMatrizA()
        print("C ORIGINAL SEM REMOVER ARTIFICIAIS")
        print("{}".format(novoC))
        indexColunaInicialVarArtificiais = novoC.shape[0] - self._tableaux.numRestricoes()

        novoC = np.delete(novoC, np.s_[indexColunaInicialVarArtificiais:], 0)
        novoA = np.delete(novoA, np.s_[indexColunaInicialVarArtificiais:], 1)

        tableaux_segunda_parte_simplex.setC(novoC)
        tableaux_segunda_parte_simplex.setMatrizA(novoA)
        tableaux_segunda_parte_simplex.setValorOtimo(self._tableaux.getValorOtimoDoCOriginal())
        tableaux_segunda_parte_simplex.setCertificadoOtimo(self._tableaux.getCertificadoOtimoDoCOriginal())

        return tableaux_segunda_parte_simplex