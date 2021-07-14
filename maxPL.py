import numpy as np

class PL():

    def __init__(self,c,b,restricoes):
        self.c = c
        self.b = b
        self.restricoes = restricoes
    
    def numRestricoes(self):
        return self.restricoes.shape[0]
    
    def numVariaveis(self):
        return self.restricoes.shape[1]
    
    def print(self):
        print("C: {}".format(self.c))
        print("B: {}".format(self.b))
        print("Restrições:\n {}".format(self.restricoes))