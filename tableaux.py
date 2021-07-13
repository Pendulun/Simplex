import numpy as np

class Tableux():
    def __init__(self):
        self.__valorOtimo = 0
        self.__certificadoOtimo = []
        self.__solucaoViavel = []
        self.__isViavel = True
        self.__isIlimitada = True
        self.__certificadoIlimitada = []
        pass

    def resolver(self):
        pass
    
    def getSolucaoViavel(self):
        if(self.__isViavel):
            return self.__solucaoViavel.copy()
    
    def getCertificadoOtimo(self):
        pass

    def getCertificadoOtimalidade(self):
        if(not self.__isIlimitada):
            return self.__certificadoOtimo
    
    def getValorOtimo(self):
        if(self.__isViavel):
            return self.__valorOtimo
    
