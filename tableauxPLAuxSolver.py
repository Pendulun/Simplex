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
        #Tratar B negativos multiplicando-os por -1 sem fazer nenhum pivoteamento
        self._verificarB()

        #Adicionar Variáveis artificiais em A
        self._adicionarVariaveisArtificiais()

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
    
    def _adicionarVariaveisArtificiais(self):
        print("ADICIONANDO VARIAVEIS ARTIFICIAIS MATRIZ A")
        variaveisArt = self.__geraMatrizIdentidade(self._tableaux.numRestricoes())
        self._tableaux.addMatrizA(variaveisArt)
        self._tableaux.print()
    
    def __geraMatrizIdentidade(self, tam):
        print("Gera Matriz Identidade")
        return np.identity(tam)

    def _zerarVariaveisArtificiaisDeC(self):
        indexPrimeiraColDeCVarArtificiais = self._tableaux.numVariaveisC() - self._tableaux.numRestricoes()

        numColDaBaseArt=0
        for i in range(indexPrimeiraColDeCVarArtificiais, self._tableaux.numVariaveisC()):
            #Já que já sei que no vetor i de A tem um elemento igual a 1
            self._adicionaLinhaNaLinhaAlvoTableauxNumVezes(numColDaBaseArt, 0,  -1)
            print("ADICIONANDO LINHA {} DE A EM C".format(numColDaBaseArt))
            self._tableaux.print()
            numColDaBaseArt+=1
    
    #Talvez isso suba para a classe pai com um nome de pivoteamento
    def _adicionaLinhaNaLinhaAlvoTableauxNumVezes(self, numLinhaOrigem, numLinhaAlvo, numVezes):
        if numLinhaAlvo != numLinhaOrigem:
            linhaA = self._tableaux.getCopiaLinhaA(numLinhaOrigem)
            linhaMTransf = self._tableaux.getCopiaLinhaMTransf(numLinhaOrigem)
            valorB = self._tableaux.getValorB(numLinhaOrigem)

            if numLinhaAlvo == 0:
                self._tableaux.addNoCertificadoOtimo(linhaMTransf*numVezes)
                self._tableaux.addNoVetorC(linhaA*numVezes)
                self._tableaux.addNoValorOtimo(valorB*numVezes)
            else:
                numLinhaCorrigidoParaRestoTableaux = numLinhaAlvo-1
                self._tableaux.addNaMatrizTransf(numLinhaCorrigidoParaRestoTableaux, linhaMTransf*numVezes)
                self._tableaux.addMatrizA(numLinhaCorrigidoParaRestoTableaux, linhaA*numVezes)
                self._tableaux.addNoVetorB(numLinhaCorrigidoParaRestoTableaux, valorB*numVezes)



