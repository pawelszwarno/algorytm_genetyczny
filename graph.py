import numpy as np
import pandas as pd


class Graph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = None
        self.list_of_vertices = [i for i in range(self.rows)]
        
    def __repr__(self):
        return self.matrix
    
    def __str__(self):
        return '{}'.format(self.matrix)

    def create_adj_matrix(self, low_value, high_value):
        if self.matrix is None:
            weighted_matrix = np.random.randint(
                high=high_value, size=(self.rows, self.cols), low=low_value)
            self.matrix = np.maximum(
                weighted_matrix, weighted_matrix.transpose())
            for i in range(self.rows):
                self.matrix[i][i] = 0
