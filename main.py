import numpy as np
from simplex import Simplex

def leEntrada():
    n, m = input().split()

    n = int(n)
    m = int(m)
    restricoes = np.zeros((n,m), dtype="float32")
    b = np.zeros(n, dtype="float32")
    c = np.array(input().split(), dtype="float32")

    for i in range(n):
        linha = np.array(list(input().split()))
        restricoes[i] = linha[:-1]
        b[i] = linha[-1]

    return c,b,restricoes

def main():
    
    c,b,restricoes=leEntrada(arquivo)
    my_simplex = Simplex(c,b,restricoes)
    my_simplex.resolver()
    my_simplex.imprimeResultado()
    
if __name__ == '__main__':
    main()