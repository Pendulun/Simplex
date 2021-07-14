import numpy as np

class PL():

    def __init__(self,c,b,restricoes):
        self.c = c
        self.b = b
        self.restricoes = restricoes
    
    def numRestricoes(self):
        return self.restricoes.shape[0]
    
    def numVariaveisRestricoes(self):
        return self.restricoes.shape[1]
    
    def numVariaveisC(self):
        return self.c.shape[0]
    
    def print(self):
        print("C: {}".format(self.c))
        print("B: {}".format(self.b))
        print("Restrições:\n {}".format(self.restricoes))
    
    def getRestricoes(self):
        return self.restricoes.copy()
    
    def setRestricoes(self,novasRestricoes):
        self.restricoes = novasRestricoes

    def getC(self):
        return self.c.copy()
    
    def setC(self, novoC):
        self.c = novoC