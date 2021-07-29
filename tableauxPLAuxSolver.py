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

    def resolver(self):

        self._tratarBNegativo()

        self._adicionarVariaveisArtificiaisEmA()

        self._zerarVariaveisArtificiaisDeC()

        self._trataCNegativo()

        return self._tableaux
    
    def  _tratarBNegativo(self):
         while True:
            indexBINegativo = self._getIndexBINegativo()
            if indexBINegativo < 0:
                break
            else:
                self._trataBiNegativo(indexBINegativo)

    def _getIndexBINegativo(self):
        b = self._tableaux.getB()
        for i in range(self._tableaux.numRestricoes()):
            if math.isclose(b[i], 0, abs_tol=self.PRECISAO):
                self._tableaux.attValorB(i, 0.0)
            elif b[i] < 0:
                return i
        return -1

    def _trataBiNegativo(self, index):
        self._multiplicaLinhaPor(index+1,-1)
    
    def _adicionarVariaveisArtificiaisEmA(self):
        variaveisArt = self.__geraMatrizIdentidade(self._tableaux.numRestricoes())
        self._tableaux.addMatrizA(variaveisArt)
    
    def __geraMatrizIdentidade(self, tam):
        return np.identity(tam)

    def _zerarVariaveisArtificiaisDeC(self):
        #Para cada linha de A, somar no vetor C
        for indexLinhaMatrizA in range(self._tableaux.numRestricoes()):
            #Já que já sei que no vetor i de A tem um elemento igual a 1
            self._adicionaLinhaMatrizANaLinhaAlvoTableauxNumVezes(indexLinhaMatrizA, 0,  -1)
    
    def _zerarColunaPeloElemento(self, indexColuna, indexLinha):
        self._zeraColunaMatrizA(indexColuna, indexLinha)
        self._zeraElementoVetorC(indexColuna, indexLinha)
        self._zeraElementoVetorCOriginal(indexColuna, indexLinha)
    
    def _zeraElementoVetorCOriginal(self, indexColuna, indexLinha):
        valorElementoASerZerado = self._tableaux.getElementoCOriginal(indexColuna)
        if math.isclose(valorElementoASerZerado, 0.0, abs_tol=self.PRECISAO):
            self._tableaux.attValorCOriginal(indexColuna, 0)
        else:
            #Assumindo que o elemento sendo pivoteado tem valor igual a 1
            valorAMultiplicarALinhaComElementoPivo = -1*valorElementoASerZerado
            self._adicionaLinhaMatrizANoCOriginalNumVezes(indexLinha,valorAMultiplicarALinhaComElementoPivo)
    
    def _adicionaLinhaMatrizANoCOriginalNumVezes(self, indexLinhaMatrizAOrigem, numVezes):
        linhaA = self._tableaux.getCopiaLinhaA(indexLinhaMatrizAOrigem)
        linhaMTransf = self._tableaux.getCopiaLinhaMTransf(indexLinhaMatrizAOrigem)
        valorB = self._tableaux.getValorB(indexLinhaMatrizAOrigem)
        self._tableaux.addNoCertificadoOtimoOriginal(linhaMTransf*numVezes)
        self._tableaux.addNoVetorCOriginal(linhaA*numVezes)
        self._tableaux.addNoValorOtimoOriginal(valorB*numVezes) 

    
    def get_tableaux_segunda_parte(self):

        tableaux_segunda_parte_simplex = Tableaux()
        tableaux_segunda_parte_simplex.copiaDoTableaux(self._tableaux)
        
        novoC = self._tableaux.getCOriginalNegativado()
        novoA = self._tableaux.getMatrizA()

        indexColunaInicialVarArtificiais = novoC.shape[0] - self._tableaux.numRestricoes()

        novoC = np.delete(novoC, np.s_[indexColunaInicialVarArtificiais:], 0)
        novoA = np.delete(novoA, np.s_[indexColunaInicialVarArtificiais:], 1)

        tableaux_segunda_parte_simplex.setC(novoC)
        tableaux_segunda_parte_simplex.setMatrizA(novoA)
        tableaux_segunda_parte_simplex.setValorOtimo(self._tableaux.getValorOtimoDoCOriginal())
        tableaux_segunda_parte_simplex.setCertificadoOtimo(self._tableaux.getCertificadoOtimoDoCOriginal())

        return tableaux_segunda_parte_simplex
    
    def getTableaux(self):
        return self._tableaux