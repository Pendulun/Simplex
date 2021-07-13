import numpy as np

def leArquivo(arquivo="standard_input.txt"):
    file = open(arquivo,"r")
    n, m = file.readline().split()

    n = int(n)
    m = int(m)
    restricoes = np.zeros((n,m), dtype="int32")
    b = np.zeros(n, dtype="int32")
    c = np.array(file.readline().split(), dtype="int32")
    
    for i in range(n):
        linha = np.array(list(file.readline().split()))
        restricoes[i] = linha[:-1]
        b[i] = linha[-1]
        
    file.close()
    return n,m,c,b,restricoes

def imprimeTudo(n,m,c,b,restricoes):
    print("Número de restrições: {}".format(n))
    print("Número de variáveis: {}".format(m))
    print("Vetor C: {}".format(c))
    print("Vetor B: {}".format(b))
    print("Restrições: {}".format(restricoes))


def trocaSinalRestricaoSeBNaoPositivo(b,restricoes):
    print("TROCA SINAL")
    for i in range(b.size):
        if b[i]<0:
            restricoes[i] = restricoes[i] * -1
            b[i] = b[i] * -1

def main():
    arquivo = "standard_input.txt"
    
    try:
        n,m,c,b,restricoes=leArquivo(arquivo)
        imprimeTudo(n,m,c,b,restricoes)
        trocaSinalRestricaoSeBNaoPositivo(b,restricoes)
        imprimeTudo(n,m,c,b,restricoes)
    except OSError:
        print("Não foi possível abrir arquivo no endereço {}".format(arquivo))
    
if __name__ == '__main__':
    main()