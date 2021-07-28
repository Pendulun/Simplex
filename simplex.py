from tableauxAux import TableauxAux
import numpy as np
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
    PRECISAO=0.0001
    

    def __init__(self,c,b,restricoes):
        self.__pl = PL(c,b,restricoes)
        self.__estadoFinal = ""

    def resolver(self):
        print("PL RECEBIDA")
        self.imprimeTudo()
        
        plEmFPI = self.__colocaPLEmFPI(self.__pl)

        print("PL ORIGINAL EM FPI")
        plEmFPI.print()

        tableauxAuxSolver = self._resolvePLAux(plEmFPI)
        tableaux_aux = tableauxAuxSolver.resolver()

        print("TABLEAUX FINAL DA PL AUXILIAR")
        tableaux_aux.print()

        if tableaux_aux.resultadoTornaPLOriginalViavel():
            
            tableaux_parte_2 = tableauxAuxSolver.get_tableaux_segunda_parte()
            print("TABLEAUX SEGUNDA PARTE:")
            tableaux_parte_2.print()

            tableaux_pl = self.__gerarTableauxResolvido(tableaux_parte_2)

            print("TABLEAUX FINAL DA PL")
            tableaux_pl.imprimirTudo()

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
    
    def __geraMatrizIdentidade(self, tam):
        print("Gera Matriz Identidade")
        return np.identity(tam)

    def _resolvePLAux(self, pl):
        plAux = self.__transformaCNaVersaoDaAuxiliar(pl)
        print("PL APOS COLOCAR C NA FORMA DA PL AUXILIAR")
        plAux.print()
        print("")

        #A plAux está sem tratar B negativo e sem A com colunas das var. Artificiais
        #O solver já cria o TableauxAux
        return TableauxPLAuxSolver(plAux, pl.getC())

    def __transformaCNaVersaoDaAuxiliar(self,pl):
        print("GERANDO PL AUXILIAR")
        plAux = pl.copia()

        #zerar o vetor C e adicionar 1's
        plAux.setC(np.zeros(plAux.numVariaveisC()))
        vetorMenosUns = np.full(plAux.numRestricoes(),-1)
        plAux.addEmC(vetorMenosUns)

        return plAux

    def __gerarTableauxResolvido(self, tableaux):
        print("GERANDO TABLEAUX RESOLVIDO")
        my_tableaux = TableauxSolver()
        my_tableaux.comBaseNoTableaux(tableaux)
        my_tableaux.resolver()
        return my_tableaux

    def imprimeTudo(self):
        self.__pl.print()
        print("Estado Final: {}".format(self.__estadoFinal))

    def imprimeResultado(self):
        print("Estado Final: {}".format(self.__estadoFinal))
        if self.__estadoFinal == self.INVIAVEL:
            print("Certificado de Inviabilidade: {}".format(self.tableauxFinal.getCertificadoOtimo()))
        elif self.__estadoFinal == self.OTIMA:
            print("Valor ótimo: {}".format(self.tableauxFinal.getValorOtimo()))
            print("Solução ótima: {}".format(self.tableauxFinal.getSolucaoViavel()))
            print("Certificado Otimalidade: {}".format(self.tableauxFinal.getCertificadoOtima()))