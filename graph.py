import numpy as np
import pandas as pd


class Graph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = None

    def create_adj_matrix(self, low_value, high_value):
        if self.matrix is None:
            weighted_matrix = np.random.randint(
                high=high_value, size=(self.rows, self.cols), low=low_value)
            self.matrix = np.maximum(
                weighted_matrix, weighted_matrix.transpose())
            # self.matrix = np.fill_diagonal(weighted_matrix_s, 0)
            for i in range(self.rows):
                self.matrix[i][i] = 0

def main():
    g = Graph(10, 10)
    g.create_adj_matrix(0, 10)
    print(g.matrix)


if __name__ == "__main__":
    main()
