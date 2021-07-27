import numpy as np
import math
from numpy.lib.index_tricks import IndexExpression
from maxPL import PL
from tableaux import Tableaux

class TableauxSolver():
    PRECISAO = 0.0001

    def __init__(self,pl):
        self._tableaux = Tableaux(pl)
        self._solucaoViavel = np.array(range(pl.numVariaveisRestricoes()))
        self._isViavel = True
        self._isIlimitada = True
        self._isOtimo = True
        self._certificadoIlimitada = np.array(range(pl.numRestricoes()))

    def imprimirTudo(self):
        print("Meu Tableaux")
        print("É Viável: {}".format(self._isViavel))
        print("É Ilimitada: {}".format(self._isIlimitada))
        print("É Ótima: {}".format(self._isOtimo))
        self._tableaux.print()
        print("Solução Viável: {}".format(self._solucaoViavel))
        print("Certificado Ilimitada: {}".format(self._certificadoIlimitada))
        
    def resolver(self):
        print("TABLEAUX INICIAL:")
        self._tableaux.print()

        #enquanto houver c[i] negativo ou b[i] negativo
        while True:
            pivoteou = False

            pivoteou = self._verificarB()

            """
            if not pivoteou:
                pivoteou = self.__verificarC()
            else:
                self.__verificarC()
            """

            #Não sei se isso está certo
            if not pivoteou:
                self._isOtimo = True
                self._isIlimitada = False
                self._isViavel = True
                break

    def _verificarB(self):
        pivoteou = False
        while True:
            indexBINegativo = self._getIndexBINegativo()
            if indexBINegativo < 0:
                break
            else:
                print("INDEX B NEGATIVO: {}".format(indexBINegativo))
                self._trataBiNegativo(indexBINegativo)
                pivoteou = True
        return pivoteou
    
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
        #pivotear elemento
        self._tableaux.print()
    
    def _trataCNegativo(self):
        print("TRATANDO CI'S NEGATIVOS")
        pivoteou = False
        while True:
            indexCINegativo = self._getIndexCINegativo()
            if indexCINegativo < 0:
                break
            else:
                print("INDEX C NEGATIVO: {}".format(indexCINegativo))
                self._trataCiNegativo(indexCINegativo)
                pivoteou = True

        return pivoteou
    
    def _getIndexCINegativo(self):
        c = self._tableaux.getC()
        for i in range(self._tableaux.numVariaveisC()):
            if math.isclose(c[i], 0, abs_tol=self.PRECISAO):
                #Define como 0.0, já que é perto mesmo
                self._tableaux.attValorC(i, 0.0)
            elif c[i] < 0:
                return i
        return -1

    def _trataCiNegativo(self,index):
        #pivotear algum elemento
        pass

    def _multiplicaLinhaPor(self,numLinhaTableaux, valor):
        if numLinhaTableaux == 0:
            self._multiplicaPrimeiraLinhaPor(valor)
        else:
            self._multiplicaLinhaRestoTableauxPor(numLinhaTableaux, valor)
    
    def _multiplicaPrimeiraLinhaPor(self,valor):
        pass

    def _multiplicaLinhaRestoTableauxPor(self,numLinha, valor):
        self._tableaux.attLinhaMatrizTransformacoes(numLinha-1,self._tableaux.getMatrizTransformacoes()[numLinha-1]*valor)
        self._tableaux.attLinhaA(numLinha-1, self._tableaux.getMatrizA()[numLinha-1]*valor)
        self._tableaux.attValorB(numLinha-1,self._tableaux.getB()[numLinha-1]*valor)

    def getSolucaoViavel(self):
        if(self._isViavel):
            return self._solucaoViavel.copy()
    
    def getCertificadoOtimalidade(self):
        if self._isOtimo:
            return self._tableaux.getCertificadoOtimo()
    
    def getValorOtimo(self):
        if(self._isViavel):
            return self._tableaux.getValorOtimo()
    
    def isViavel(self):
        return self._isViavel
    
    def isIlimitada(self):
        return self._isIlimitada
    
    def isOtima(self):
        return self._isOtimo

    def getCertificadoIlimitada(self):
        if self._isIlimitada:
            return self._certificadoIlimitada.copy()
    
    def getCertificadoOtima(self):
        if self._isOtimo:
            return self._certificadoOtimo.copy()
    
    def getTableaux(self):
        return self._tableaux
