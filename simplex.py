import numpy as np
import math
from maxPL import PL
from tableauxSolver import TableauxSolver
from tableauxPLAuxSolver import TableauxPLAuxSolver

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
    PRECISAO = 0.0001
    

    def __init__(self,c,b,restricoes):
        self.__pl = PL(c,b,restricoes)
        self.__estadoFinal = ""

    def resolver(self):
        print("PL RECEBIDA")
        self.imprimeTudo()
        tableaux_aux = self.__geraTableauxPLAuxiliarDaPL(self.__pl)
        print("TABLEAUX FINAL DA PL AUXILIAR")
        tableaux_aux.imprimirTudo()
        if math.isclose(tableaux_aux.getValorOtimo(),0,abs_tol=self.PRECISAO):
            print("É VIÁVEL")
            plEmFPI = self.__colocaPLEmFPI(self.__pl)
            print("PL ORIGINAL EM FPI")
            plEmFPI.print()

            #gerar Tableaux Resolvido
            tableaux_pl = self.__gerarTableauxResolvido(plEmFPI)
            print("TABLEAUX FINAL DA PL")
            tableaux_pl.imprimirTudo()

            #confere estado do tableaux resolvido
            if tableaux_pl.isOtima():
                print("É ÓTIMA")
                self.__estadoFinal = self.OTIMA
            elif tableaux_pl.isIlimitada():
                print("É ILIMITADA")
                self.__estadoFinal = self.ILIMITADA

            self.tableauxFinal = tableaux_pl
        else:
            print("NÃO É VIÁVEL")
            self.__estadoFinal = self.INVIAVEL
            self.tableauxFinal = tableaux_aux

    def __geraTableauxPLAuxiliarDaPL(self, pl):
        print("GERA TABLEAUX DA PL AUXILIAR DA PL")
        plAux = self.__geraPLAuxiliar(pl)
        #print("PL AUX GERADA:")
        #plAux.print() 
        return self.__gerarTableauxAuxResolvido(plAux, pl.getC())

    def __gerarTableauxAuxResolvido(self, pl, cOriginal):
        print("GERANDO TABLEAUX RESOLVIDO")
        my_tableaux = TableauxPLAuxSolver(pl, cOriginal)
        my_tableaux.resolver()
        return my_tableaux

    def __gerarTableauxResolvido(self, pl):
        print("GERANDO TABLEAUX RESOLVIDO")
        my_tableaux = TableauxSolver(pl)
        my_tableaux.resolver()
        return my_tableaux

    def __geraPLAuxiliar(self,pl):
        print("GERANDO PL AUXILIAR")
        #Criar nova PL Auxiliar com base na original
        plAux = pl.copia()
        plAux.setC(np.zeros(plAux.numVariaveisC()))

        #Trata B negativo
        plAux = self.__trataBNegativoPL(plAux)

        #Adicionar matriz de variáveis de folga nas restrições
        variaveisAux = self.__geraMatrizIdentidade(plAux.numRestricoes())
        plAux.setRestricoes(np.hstack((plAux.getRestricoes(),variaveisAux)))

        #zerar o vetor C e adicionar 1's
        vetorUns = np.full(abs(plAux.getDiferencaNumVariaveisCERestricoes()),-1)
        plAux.setC(np.concatenate((plAux.getC(),vetorUns), axis=None))

        #retorna PL Auxiliar
        return plAux

    def __trataBNegativoPL(self,plAux):
        b = plAux.getB()
        restricoes = plAux.getRestricoes()
        for i in range(plAux.numRestricoes()):
            if math.isclose(b[i], 0, abs_tol=self.PRECISAO):
                #Define como 0.0, já que é perto mesmo
                plAux.attValorB(i, 0.0)
            elif b[i] < 0:
                # Multiplica b[i] e restricoes[i] por -1
                plAux.attValorB(i,b[i]*-1)
                plAux.attLinhaRestricoes(i,restricoes[i]*-1)
        return plAux 

    def __colocaPLEmFPI(self, pl):
        print("COLOCANDO EM FPI")
        plCopia = pl.copia()

        #Adicionar matriz de variáveis de folga nas restrições
        variaveisAux = self.__geraMatrizIdentidade(plCopia.numRestricoes())
        plCopia.setRestricoes(np.hstack((plCopia.getRestricoes(),variaveisAux)))

        #completar o vetor C com 0's
        vetorZeros = np.zeros(plCopia.numVariaveisRestricoes()-plCopia.numVariaveisC())
        plCopia.setC(np.concatenate((plCopia.getC(),vetorZeros), axis=None))
        return plCopia
    
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
    
    def __geraMatrizIdentidade(self, tam):
        print("Gera Matriz Identidade")
        return np.identity(tam)
