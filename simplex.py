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
    def __init__(self,c,b,restricoes):
        self.pl = PL(c,b,restricoes)

    def resolver(self):
        print("PL RECEBIDA")
        self.imprimeTudo()
        if(self.__verificaViabilidade()):
            pass
        else:
            pass
        

    def __verificaViabilidade(self):
        plAux = self.__geraPLAuxiliar()
        print("PL AUX:")
        plAux.print()
        my_tableaux = Tableaux(plAux)
        my_tableaux.resolver()
        my_tableaux.imprimirTudo()
        if(my_tableaux.getValorOtimo() < 0):
            return False
        elif(my_tableaux.getValorOtimo() > 0):
            print("Algo deu errado! Valor ótimo da PL Auxiliar é maior que 0!")
        else:
            return True

    def __geraPLAuxiliar(self):
        print("Gerando PL Auxiliar")
        #Criar nova PL Auxiliar com base na original
        cAux = np.zeros(self.pl.c.shape[0])
        bAux = self.pl.b.copy()
        restricoesAux = self.pl.restricoes.copy()

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
        self.pl.print()

    def __trocaSinalLinhaSeBNaoPositivo(self):
        print("TROCA SINAL")
        for i in range(self.b.size):
            if self.b[i]<0:
                self.restricoes[i] = self.restricoes[i] * -1
                self.b[i] = self.b[i] * -1
    
    def __geraMatrizIdentidade(self, tam):
        print("Gera Matriz Identidade")
        return np.identity(tam)
