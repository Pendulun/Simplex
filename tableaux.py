import numpy as np

class Tableux():
    def __init__(self,c,b,restricoes):
        self.__valorOtimo = 0
        self.__certificadoOtimo = np.array(range(restricoes.shape[0]))
        self.__solucaoViavel = np.array(range(restricoes.shape[0]))
        self.__isViavel = True
        self.__isIlimitada = True
        self.__certificadoIlimitada = np.array(range(restricoes.shape[0]))
        self.__matrizTransformacoes = np.identity(restricoes.shape[0])

    def imprimirTudo(self):
        print("Meu Tableaux")
        print("Valor Ótimo: {}".format(self.__valorOtimo))
        print("Certificado Ótimo: {}".format(self.__certificadoOtimo))
        print("Solução Viável: {}".format(self.__solucaoViavel))
        print("É Viável: {}".format(self.__isViavel))
        print("É Ilimitada: {}".format(self.__isIlimitada))
        print("Certificado Ilimitada: {}".format(self.__certificadoIlimitada))
        print("Matriz Transformações: {}".format(self.__matrizTransformacoes))

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
    
