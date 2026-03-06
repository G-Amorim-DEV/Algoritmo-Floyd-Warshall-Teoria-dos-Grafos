import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import argparse


def plot_heatmap(matrix, title='Menores distâncias entre vértices'):
    # Accept either list of lists or pandas DataFrame
    if not isinstance(matrix, pd.DataFrame):
        matrix = pd.DataFrame(matrix)

    sns.heatmap(matrix, annot=True, cmap='coolwarm')
    plt.title(title)
    plt.show()


def read_csv(path):
    return pd.read_csv(path, header=None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dist', help='CSV de distâncias', required=True)
    args = parser.parse_args()
    df = read_csv(args.dist)
    plot_heatmap(df)


if __name__ == '__main__':
    main()