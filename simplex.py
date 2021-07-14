import numpy as np
from maxPL import PL
from tableaux import Tableaux

class Simplex():
    """
    Essa classe tem o objetivo de ser um Solver para PL's no seguinte formato:
    max c_T*X
    sujeito a AX <= b e X>=0
    aplicando  o algoritmo Simplex
    """
    OTIMA = "otima"
    INVIAVEL = "inviavel"
    ILIMITADA = "ilimitada"
    tableauxFinal = ""
    

    def __init__(self,c,b,restricoes):
        self.__pl = PL(c,b,restricoes)
        self.__estadoFinal = ""

    def resolver(self):
        print("PL RECEBIDA")
        self.imprimeTudo()
        #Se a PL auxiliar é inviável, salve as informações do estado e o certificado de inviabilidade
        tableaux_aux = self.__geraTableauxPLAuxiliarDaPL(self.__pl)
        if tableaux_aux.getValorOtimo() == 0:
            print("É VIÁVEL")
            self.__estadoFinal = self.OTIMA
            #Isso aqui embaixo deve ser trocado pelo tableaux da resolução final
            self.tableauxFinal = tableaux_aux
        else:
            print("NÃO É VIÁVEL")
            self.__estadoFinal = self.INVIAVEL
            self.tableauxFinal = tableaux_aux

    def __geraTableauxPLAuxiliarDaPL(self, pl):
        print("GERA TABLEAUX DA PL AUXILIAR DA PL")
        plAux = self.__geraPLAuxiliar(pl)
        print("PL AUX GERADA:")
        plAux.print()
        my_tableaux = self.__gerarTableauxResolvido(plAux)
        return my_tableaux

    def __gerarTableauxResolvido(self, pl):
        print("GERANDO TABLEAUX RESOLVIDO")
        my_tableaux = Tableaux(pl)
        my_tableaux.resolver()
        return my_tableaux

    def __geraPLAuxiliar(self,pl):
        print("GERANDO PL AUXILIAR")
        #Criar nova PL Auxiliar com base na original
        cAux = np.zeros(pl.c.shape[0])
        bAux = pl.b.copy()
        restricoesAux = pl.restricoes.copy()

        #Adicionar matriz de variáveis de folga nas restrições
        print(restricoesAux.shape[0])
        variaveisAux = self.__geraMatrizIdentidade(restricoesAux.shape[0])
        restricoesAux = np.hstack((restricoesAux,variaveisAux))

        #zerar o vetor C e adicionar 1's
        vetorUns = np.ones(restricoesAux.shape[0])
        cAux = np.concatenate((cAux,vetorUns), axis=None)

        #retorna PL Auxiliar
        return PL(cAux, bAux, restricoesAux)

    def imprimeTudo(self):
        self.__pl.print()
        print("Estado Final: {}".format(self.__estadoFinal))
    
    def imprimeResultado(self):
        print("Estado Final: {}".format(self.__estadoFinal))
        if self.__estadoFinal == self.INVIAVEL:
            print("Certificado de Inviabilidade: {}".format(self.tableauxFinal.getCertificadoOtimalidade()))
        elif self.__estadoFinal == self.OTIMA:
            print("Valor ótimo: {}".format(self.tableauxFinal.getValorOtimo()))
            print("Solução ótima: {}".format(self.tableauxFinal.getSolucaoViavel()))
            print("Certificado Otimalidade: {}".format(self.tableauxFinal.getCertificadoOtimalidade()))

    def __trocaSinalLinhaSeBNaoPositivo(self):
        print("TROCA SINAL")
        for i in range(self.b.size):
            if self.b[i]<0:
                self.restricoes[i] = self.restricoes[i] * -1
                self.b[i] = self.b[i] * -1
    
    def __geraMatrizIdentidade(self, tam):
        print("Gera Matriz Identidade")
        return np.identity(tam)
