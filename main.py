import argparse
import pandas as pd
import numpy as np
import floyd


def read_matrix(path):
    df = pd.read_csv(path, header=None)
    return df.values.tolist()


def main():
    parser = argparse.ArgumentParser(description="Floyd-Warshall CLI")
    parser.add_argument("-n", "--vertices", type=int, help="Número de vértices")
    parser.add_argument("--dist", help="CSV com a matriz de distâncias")
    parser.add_argument("--pred", help="CSV com a matriz de predecessores")

    args = parser.parse_args()

    if args.dist and args.pred:
        dist = read_matrix(args.dist)
        pred = read_matrix(args.pred)
        n = len(dist)
    else:
        n = args.vertices or int(input('Numero de vertices: '))
        print('Digite a matriz de distancias')
        dist = []
        for i in range(n):
            linha = list(map(int, input().split()))
            dist.append(linha)

        print('Digite a de precedencia')
        pred = []
        for i in range(n):
            linha = list(map(int, input().split()))
            pred.append(linha)

    dist, pred = floyd.floyd_warshall(dist, pred)

    df_dist = pd.DataFrame(dist)
    df_pred = pd.DataFrame(pred)

    print('\nMatriz final de distancias')
    print(df_dist)
    print('\nMatriz final de precedencia')
    print(df_pred)


if __name__ == '__main__':
    main()

