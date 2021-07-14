import numpy as np
from maxPL import PL

class Tableaux():
    def __init__(self,pl):
        self.__valorOtimo = 0
        self.__certificadoOtimo = np.array(range(pl.numRestricoes()))
        self.__solucaoViavel = np.array(range(pl.numVariaveisRestricoes()))
        self.__isViavel = True
        self.__isIlimitada = True
        self.__isOtimo = True
        self.__certificadoIlimitada = np.array(range(pl.numRestricoes()))
        self.__matrizTransformacoes = np.identity(pl.numRestricoes())
        self.__pl = pl

    def imprimirTudo(self):
        print("Meu Tableaux")
        print("Valor Ótimo: {}".format(self.__valorOtimo))
        print("Certificado Ótimo: {}".format(self.__certificadoOtimo))
        print("Solução Viável: {}".format(self.__solucaoViavel))
        print("É Viável: {}".format(self.__isViavel))
        print("É Ilimitada: {}".format(self.__isIlimitada))
        print("Certificado Ilimitada: {}".format(self.__certificadoIlimitada))
        print("Matriz Transformações:\n {}".format(self.__matrizTransformacoes))
        print("PL:")
        self.__pl.print()

    def resolver(self):
        pass

    def getSolucaoViavel(self):
        if(self.__isViavel):
            return self.__solucaoViavel.copy()
    
    def getCertificadoOtimalidade(self):
        if self.__isOtimo:
            return self.__certificadoOtimo.copy()
    
    def getValorOtimo(self):
        if(self.__isViavel):
            return self.__valorOtimo
    
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
    
