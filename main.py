import numpy as np

def leArquivo(arquivo="standard_input.txt"):
    file = open(arquivo,"r")
    n, m = file.readline().split()

    n = int(n)
    m = int(m)
    restricoes = []
    b = []
    c = file.readline().split()

    for i in range(n):
        linha = list(file.readline().split())
        restricoes.append(linha[:-1])
        b.append(linha[-1])
        
    file.close()
    return n,m,c,b,restricoes

def main():
    arquivo = "standard_input.txt"
    try:
        n,m,c,b,restricoes=leArquivo(arquivo)
        print("Número de restrições: {}".format(n))
        print("Número de variáveis: {}".format(m))
        print("Vetor C: {}".format(c))
        print("Vetor B: {}".format(b))
        print("Restrições: {}".format(restricoes))
    except:
        print("Não foi possível abrir arquivo no endereço {}".format(arquivo))
    
if __name__ == '__main__':
    main()