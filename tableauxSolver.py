import numpy as np
import math
from numpy.lib.index_tricks import IndexExpression
from maxPL import PL
from tableaux import Tableaux

class TableauxSolver():
    PRECISAO = 0.0001

    def comBaseNaPl(self, pl):
        self._tableaux = Tableaux()
        self._tableaux.setPL(pl)
        self._solucaoViavel = np.array(range(pl.numVariaveisRestricoes()))
        self._isViavel = True
        self._isIlimitada = True
        self._isOtimo = True
        self._certificadoIlimitada = np.array(range(pl.numRestricoes()))
    
    def comBaseNoTableaux(self, tableaux):
        self._tableaux = tableaux
        self._solucaoViavel = np.array(range(self._tableaux.numRestricoes()))
        self._isViavel = True
        self._isIlimitada = True
        self._isOtimo = True
        self._certificadoIlimitada = np.array(range(self._tableaux.numRestricoes()))

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

            #Não preciso verificar B negativo pois já foi feito no Tableaux Aux (?)


            """
            pivoteou = self.__verificarC()
            """

            #Não sei se isso está certo
            if not pivoteou:
                self._isOtimo = True
                self._isIlimitada = False
                self._isViavel = True
                break
    
    def _trataCNegativo(self):
        print("TRATANDO CI'S NEGATIVOS")
        pivoteou = False
        while True:
            indexCINegativo = self._getIndexCINegativo()
            if indexCINegativo < 0:
                break
            else:
                print("INDEX C NEGATIVO: {}".format(indexCINegativo))
                if(self._trataCiNegativo(indexCINegativo)):
                    #Não foi possível pivotear ninguém. PL é Ilimitada
                    pass
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

    def _trataCiNegativo(self,indexElementoC):
        indexElementoAPivotear = self._escolherElementoAPivotearNaColuna(indexElementoC)
        if(indexElementoAPivotear == -1):
            return False 
        else:
            self._pivotearElementoDeA(indexElementoC, indexElementoAPivotear)
            print("TABLEAUX DEPOIS DE PIVOTEAR O ELEMENTO:")
            self._tableaux.print()
            return True
    
    def _escolherElementoAPivotearNaColuna(self,indexColuna):
        print("ESCOLHENDO ELEMENTO A SER PIVOTEADO DA COLUNA {} da matriz A".format(indexColuna))
        indexElementoASerPivoteado = -1
        matrizA = self._tableaux.getMatrizA()
        vetorB = self._tableaux.getB()
        menorRazao = np.Infinity
        for i in range(self._tableaux.numRestricoes()):
            valorAtual = matrizA[i][indexColuna]
            print("ELEMENTO matrizA{}{} = {}".format(i,indexColuna,valorAtual))
            if(valorAtual>0):
                razaoComB= (vetorB[i])/valorAtual
                if(razaoComB < menorRazao):
                    menorRazao = razaoComB
                    indexElementoASerPivoteado=i
        valorDoElemento = matrizA[indexElementoASerPivoteado][indexColuna]
        print("ELEMENTO ESCOLHIDO: matrizA{}{} = {}".format(indexElementoASerPivoteado,indexColuna,valorDoElemento))
        return indexElementoASerPivoteado
    
    def _pivotearElementoDeA(self, indexColuna, indexLinha):
        if math.isclose(self._tableaux.getElementoA(indexLinha, indexColuna), 1, abs_tol=self.PRECISAO):
            self._tableaux.attElementoA(indexLinha,indexColuna,1)
        else:
            self._transformarElementoEmUm(indexColuna, indexLinha)
        self._zerarColunaPeloElemento(indexColuna, indexLinha)
    
    def _transformarElementoEmUm(self, indexColuna, indexLinha):
        self._multiplicaLinhaPor(indexLinha+1, (1/self._tableaux.getElementoA(indexLinha, indexColuna)))

    def _zerarColunaPeloElemento(self, indexColuna, indexLinha):
        #zerando coluna matriz A
        for i in range(self._tableaux.numRestricoes()):
            if i != indexLinha:
                valorElementoASerZerado = self._tableaux.getElementoA(i,indexColuna)
                if math.isclose(valorElementoASerZerado, 0.0, abs_tol=self.PRECISAO):
                    self._tableaux.attElementoA(i, indexColuna, 0)
                else:
                    #Assumindo que o elemento sendo pivoteado tem valor igual a 1
                    valorAMultiplicarALinhaComElementoPivo = -1*valorElementoASerZerado
                    linhaAtualRelativaAoTableauxInteiro = i+1
                    self._adicionaLinhaMatrizANaLinhaAlvoTableauxNumVezes(indexLinha,linhaAtualRelativaAoTableauxInteiro,valorAMultiplicarALinhaComElementoPivo)

        #Zerando elemento vetor c
        valorElementoASerZerado = self._tableaux.getElementoC(indexColuna)
        if math.isclose(valorElementoASerZerado, 0.0, abs_tol=self.PRECISAO):
            self._tableaux.attValorC(indexColuna, 0)
        else:
            #Assumindo que o elemento sendo pivoteado tem valor igual a 1
            valorAMultiplicarALinhaComElementoPivo = -1*valorElementoASerZerado
            linhaAtualRelativaAoTableauxInteiro = 0
            self._adicionaLinhaMatrizANaLinhaAlvoTableauxNumVezes(indexLinha,linhaAtualRelativaAoTableauxInteiro,valorAMultiplicarALinhaComElementoPivo)
    
    #Talvez isso suba para a classe pai na parte de pivoteamento
    def _adicionaLinhaMatrizANaLinhaAlvoTableauxNumVezes(self, indexLinhaMatrizAOrigem, numLinhaAlvo, numVezes):
        if numLinhaAlvo != indexLinhaMatrizAOrigem+1:
            linhaA = self._tableaux.getCopiaLinhaA(indexLinhaMatrizAOrigem)
            linhaMTransf = self._tableaux.getCopiaLinhaMTransf(indexLinhaMatrizAOrigem)
            valorB = self._tableaux.getValorB(indexLinhaMatrizAOrigem)

            if numLinhaAlvo == 0:
                print("LINHA ALVO EH O C")
                self._tableaux.addNoCertificadoOtimo(linhaMTransf*numVezes)
                self._tableaux.addNoVetorC(linhaA*numVezes)
                self._tableaux.addNoValorOtimo(valorB*numVezes)
            else:
                numLinhaCorrigidoParaRestoTableaux = numLinhaAlvo-1
                self._tableaux.addNaMatrizTransf(numLinhaCorrigidoParaRestoTableaux, linhaMTransf*numVezes)
                self._tableaux.addMatrizA(numLinhaCorrigidoParaRestoTableaux, linhaA*numVezes)
                self._tableaux.addNoVetorB(numLinhaCorrigidoParaRestoTableaux, valorB*numVezes)

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
            return self._tableaux.getCertificadoOtimo()
    
    def getTableaux(self):
        return self._tableaux
