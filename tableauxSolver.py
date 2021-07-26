import numpy as np
import math
from numpy.lib.index_tricks import IndexExpression
from maxPL import PL
from tableaux import Tableaux

class TableauxSolver():
    PRECISAO = 0.0001

    def __init__(self,pl):
        self.__tableaux = Tableaux(pl)
        self.__solucaoViavel = np.array(range(pl.numVariaveisRestricoes()))
        self.__isViavel = True
        self.__isIlimitada = True
        self.__isOtimo = True
        self.__certificadoIlimitada = np.array(range(pl.numRestricoes()))

    def imprimirTudo(self):
        print("Meu Tableaux")
        print("É Viável: {}".format(self.__isViavel))
        print("É Ilimitada: {}".format(self.__isIlimitada))
        print("É Ótima: {}".format(self.__isOtimo))
        self.__tableaux.print()
        print("Solução Viável: {}".format(self.__solucaoViavel))
        print("Certificado Ilimitada: {}".format(self.__certificadoIlimitada))
        
    def resolver(self):
        print("TABLEAUX INICIAL:")
        self.__tableaux.print()

        #enquanto houver c[i] negativo ou b[i] negativo
        while True:
            pivoteou = False

            pivoteou = self.__verificarB()

            """
            if not pivoteou:
                pivoteou = self.__verificarC()
            else:
                self.__verificarC()
            """

            #Não sei se isso está certo
            if not pivoteou:
                self.__isOtimo = True
                self.__isIlimitada = False
                self.__isViavel = True
                break

    def __verificarB(self):
        pivoteou = False
        while True:
            indexBINegativo = self.__getIndexBINegativo()
            if indexBINegativo < 0:
                break
            else:
                print("INDEX B NEGATIVO: {}".format(indexBINegativo))
                self.__trataBiNegativo(indexBINegativo)
                pivoteou = True
        return pivoteou
    
    def __getIndexBINegativo(self):
        b = self.__tableaux.getB()
        for i in range(self.__tableaux.numRestricoes()):
            if math.isclose(b[i], 0, abs_tol=self.PRECISAO):
                #Define como 0.0, já que é perto mesmo
                self.__tableaux.attValorB(i, 0.0)
            elif b[i] < 0:
                return i
        return -1

    def __trataBiNegativo(self, index):
        self.__multiplicaLinhaPor(index+1,-1)
        #pivotear elemento
        self.__tableaux.print()
    
    def __verificarC(self):
        pivoteou = False
        while True:
            indexCINegativo = self.__getIndexCINegativo()
            if indexCINegativo < 0:
                break
            else:
                print("INDEX C NEGATIVO: {}".format(indexCINegativo))
                self.__trataCiNegativo(indexCINegativo)
                pivoteou = True

        return pivoteou
    
    def __getIndexCINegativo(self):
        c = self.__tableaux.getC()
        for i in range(self.__tableaux.numVariaveisC()):
            if math.isclose(c[i], 0, abs_tol=self.PRECISAO):
                #Define como 0.0, já que é perto mesmo
                self.__tableaux.attValorC(i, 0.0)
            elif c[i] < 0:
                return i
        return -1

    def __trataCiNegativo(self,index):
        #pivotear algum elemento
        pass

    def __multiplicaLinhaPor(self,numLinhaTableaux, valor):
        if numLinhaTableaux == 0:
            self.__multiplicaPrimeiraLinhaPor(valor)
        else:
            self.__multiplicaLinhaRestoTableauxPor(numLinhaTableaux, valor)
    
    def __multiplicaPrimeiraLinhaPor(self,valor):
        pass

    def __multiplicaLinhaRestoTableauxPor(self,numLinha, valor):
        self.__tableaux.attLinhaMatrizTransformacoes(numLinha-1,self.__tableaux.getMatrizTransformacoes()[numLinha-1]*valor)
        self.__tableaux.attLinhaA(numLinha-1, self.__tableaux.getMatrizA()[numLinha-1]*valor)
        self.__tableaux.attValorB(numLinha-1,self.__tableaux.getB()[numLinha-1]*valor)

    def getSolucaoViavel(self):
        if(self.__isViavel):
            return self.__solucaoViavel.copy()
    
    def getCertificadoOtimalidade(self):
        if self.__isOtimo:
            return self.__tableaux.getCertificadoOtimo()
    
    def getValorOtimo(self):
        if(self.__isViavel):
            return self.__tableaux.getValorOtimo()
    
    def isViavel(self):
        return self.__isViavel
    
    def isIlimitada(self):
        return self.__isIlimitada
    
    def isOtima(self):
        return self.__isOtimo

    def getCertificadoIlimitada(self):
        if self.__isIlimitada:
            return self.__certificadoIlimitada.copy()
    
    def getCertificadoOtima(self):
        if self.__isOtimo:
            return self.__certificadoOtimo.copy()
    
    def getTableaux(self):
        return self.__tableaux
