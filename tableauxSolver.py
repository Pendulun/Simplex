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
        self._defineEstadoInicial()
    
    def comBaseNoTableaux(self, tableaux):
        self._tableaux = tableaux
        self._defineEstadoInicial()
    
    def _defineEstadoInicial(self):
        self._solucaoViavel = np.zeros(self._tableaux.numVariaveisC())
        self._isViavel = False
        self._isIlimitada = False
        self._isOtimo = False
        self.__indexColunasBaseDict = {}
        self._indexColunaInicialVarFolga = self._tableaux.numVariaveisC() - self._tableaux.numRestricoes()
        self._certificadoIlimitada = np.zeros(self._indexColunaInicialVarFolga)

    def imprimirTudo(self):
        print("Meu Tableaux")
        print("É Viável: {}".format(self._isViavel))
        print("É Ilimitada: {}".format(self._isIlimitada))
        print("É Ótima: {}".format(self._isOtimo))
        self._tableaux.print()
        print("Solução Viável: {}".format(self._solucaoViavel))
        print("Certificado Ilimitada: {}".format(self._certificadoIlimitada))
        
    def resolver(self):

        #Não preciso verificar B negativo pois já foi feito no Tableaux Aux
        self._trataCNegativo()

        self._produzSolucaoViavel()
        #Não sei se isso está certo
        if self._isIlimitada:
            self._isOtimo = False
            self._isViavel = True
            self._produzCertificadoIlimitada()
        else:
            self._isOtimo = True
            self._isIlimitada = False
            self._isViavel = True

    def _produzCertificadoIlimitada(self):
        if self.__indexColunaATodaNegativa < len(self._certificadoIlimitada):
            self._certificadoIlimitada[self.__indexColunaATodaNegativa]=1
        colunaTodaNegativa = self._tableaux._matrizA[:,self.__indexColunaATodaNegativa]
        for i in range(self._tableaux.numRestricoes()):
            indexColunaNaBase = self.__indexColunasBaseDict.get(i,-1)
            if(indexColunaNaBase != -1):
                self._certificadoIlimitada[indexColunaNaBase] = -1*colunaTodaNegativa[i]

    def _produzSolucaoViavel(self):
        matrizCanonica = np.eye(self._tableaux.numRestricoes())
        self._solucaoViavel = np.zeros(self._tableaux.numVariaveisC()-self._tableaux.numRestricoes())
        for i in range(self._indexColunaInicialVarFolga):
            if self._colunaEstaNaBase(i, matrizCanonica):
                indexElementoUm = self._getIndexElementoUm(self._tableaux._matrizA[:,i])
                self._solucaoViavel[i] = self._tableaux.getValorB(indexElementoUm)
                self.__indexColunasBaseDict[indexElementoUm]=i
    
    def _getIndexElementoUm(self, vetor):
        for i in range(vetor.shape[0]):
            if math.isclose(vetor[i], 1, abs_tol=self.PRECISAO):
                return i
        return -1
    
    def _colunaEstaNaBase(self, indexColuna, matrizCanonica):
        if math.isclose(self._tableaux.getElementoC(indexColuna), 0, abs_tol=self.PRECISAO):
            return self._seColunaDeACanonico(indexColuna, matrizCanonica)
        else:
            return False 

    def _seColunaDeACanonico(self, indexColuna, matrizCanonica):
        coluna = self._tableaux._matrizA[:,indexColuna]

        for i in range(matrizCanonica.shape[0]):
            comparison = coluna == matrizCanonica[:,i]
            if comparison.all():
                return True
        return False
        

    def _trataCNegativo(self):
        while True:
            indexCINegativo = self._getIndexCINegativo()
            if indexCINegativo < 0:
                break
            else:
                if(not self._trataCiNegativo(indexCINegativo)):
                    self._isIlimitada = True
                    self.__indexColunaATodaNegativa = indexCINegativo
                    break
    
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
            return True
    
    def _escolherElementoAPivotearNaColuna(self,indexColuna):
        indexElementoASerPivoteado = -1
        matrizA = self._tableaux.getMatrizA()
        vetorB = self._tableaux.getB()
        menorRazao = np.Infinity
        for i in range(self._tableaux.numRestricoes()):
            valorAtual = matrizA[i][indexColuna]
            if(valorAtual>0):
                razaoComB= (vetorB[i])/valorAtual
                if(razaoComB < menorRazao):
                    menorRazao = razaoComB
                    indexElementoASerPivoteado=i
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
        self._zeraColunaMatrizA(indexColuna, indexLinha)
        self._zeraElementoVetorC(indexColuna, indexLinha)

    def _zeraColunaMatrizA(self, indexColuna, indexLinha):
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
    
    def _zeraElementoVetorC(self, indexColuna, indexLinha):
        valorElementoASerZerado = self._tableaux.getElementoC(indexColuna)
        if math.isclose(valorElementoASerZerado, 0.0, abs_tol=self.PRECISAO):
            self._tableaux.attValorC(indexColuna, 0)
        else:
            #Assumindo que o elemento sendo pivoteado tem valor igual a 1
            valorAMultiplicarALinhaComElementoPivo = -1*valorElementoASerZerado
            linhaAtualRelativaAoTableauxInteiro = 0
            self._adicionaLinhaMatrizANaLinhaAlvoTableauxNumVezes(indexLinha,linhaAtualRelativaAoTableauxInteiro,valorAMultiplicarALinhaComElementoPivo)
    
    def _adicionaLinhaMatrizANaLinhaAlvoTableauxNumVezes(self, indexLinhaMatrizAOrigem, numLinhaAlvo, numVezes):
        if numLinhaAlvo != indexLinhaMatrizAOrigem+1:
            linhaA = self._tableaux.getCopiaLinhaA(indexLinhaMatrizAOrigem)
            linhaMTransf = self._tableaux.getCopiaLinhaMTransf(indexLinhaMatrizAOrigem)
            valorB = self._tableaux.getValorB(indexLinhaMatrizAOrigem)

            if numLinhaAlvo == 0:
                self._tableaux.addNoCertificadoOtimo(linhaMTransf*numVezes)
                self._tableaux.addNoVetorC(linhaA*numVezes)
                self._tableaux.addNoValorOtimo(valorB*numVezes)
            else:
                numLinhaCorrigidoParaRestoTableaux = numLinhaAlvo-1
                self._tableaux.addNaMatrizTransf(numLinhaCorrigidoParaRestoTableaux, linhaMTransf*numVezes)
                self._tableaux.addNaMatrizA(numLinhaCorrigidoParaRestoTableaux, linhaA*numVezes)
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