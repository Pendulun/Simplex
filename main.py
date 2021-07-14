import numpy as np
from simplex import Simplex

def leArquivo(arquivo="standard_input.txt"):
    file = open(arquivo,"r")
    n, m = file.readline().split()

    n = int(n)
    m = int(m)
    restricoes = np.zeros((n,m), dtype="float32")
    b = np.zeros(n, dtype="float32")
    c = np.array(file.readline().split(), dtype="float32")

    for i in range(n):
        linha = np.array(list(file.readline().split()))
        restricoes[i] = linha[:-1]
        b[i] = linha[-1]
        
    file.close()
    return c,b,restricoes

def main():
    arquivo = "testes/standard_input2.txt"
    
    try:
        c,b,restricoes=leArquivo(arquivo)
        my_simplex = Simplex(c,b,restricoes)
        my_simplex.resolver()
    except OSError:
        print("Não foi possível abrir arquivo no endereço {}".format(arquivo))
    
if __name__ == '__main__':
    main()