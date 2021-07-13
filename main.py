import numpy as np

def leArquivo(arquivo="standard_input.txt"):
    file = open(arquivo,"r")
    n, m = file.readline().split()

    n = int(n)
    m = int(m)
    linhas = []
    c = file.readline().split()

    for i in range(n):
        linhas.append(list(file.readline().split()))
        
    file.close()
    return n,m,c,linhas

def main():
    arquivo = "standard_input.txt"
    try:
        n,m,c,linhas=leArquivo(arquivo)
        print(n)
        print(m)
        print(c)
        print(linhas)
    except:
        print("Não foi possível abrir arquivo no endereço {}".format(arquivo))
    
if __name__ == '__main__':
    main()