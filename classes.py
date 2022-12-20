#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from random import randint
from random import choice
from enum import Enum
import variables



class TruckType(Enum):
    SMALL = 1
    LARGE = 2


class Order:
    unique = 0

    def __init__(self, graph, n_pallets: int=None, max_pallets: int=10, vertex: int=None, deadline: int=None):
        self.index = self.unique
        if n_pallets is None:
            self.n_pallets = randint(1, max_pallets)
        else:
            self.n_pallets = n_pallets

        if vertex is None:
            self.vertex = choice(graph.list_of_vertices)
        else:
            self.vertex = vertex
        # deadline dany jako losowa liczba godzin od czasu startwoego 0:
        # czyli np. deadline 32 znaczy 1 dzień i 8h po rozpoczęciu mięsiąca
        # naszego horyzontu czasowego.
        self.deadline = randint(1, variables.SIMULATION_TIME)
        self.__class__.unique += 1

    def __repr__(self):
        return f'(id={self.index}, v={self.vertex}, n_p={self.n_pallets}, dl={self.deadline})'

    def __str__(self):
        return f'(id={self.index}, v={self.vertex}, n_p={self.n_pallets})'


class SolutionTuple:
    def __init__(self,n_order,n_pallets):
        # TODO: zamień n_order na zamówienie
        self.n_order = n_order
        self.n_pallets = n_pallets

    def __repr__(self):
        return f'({self.n_order}, {self.n_pallets})'

    def __str__(self):
        return f'({self.n_order}, {self.n_pallets})'


class Truck:
    unique = 0
    
    def __init__(self, type: TruckType):
        # TODO: Dodaj pamiętanie pozycji przez ciężarówkę
        self.type = type
        self.index = self.unique
        if type == TruckType.SMALL:
            self.speed = variables.speed_s
            self.capacity = variables.capacity_s
        elif type == TruckType.LARGE:
            self.speed = variables.speed_l
            self.capacity = variables.capacity_l
        self.__class__.unique += 1
        self.current_time = 0
        self.current_capacity = self.capacity
        self.current_pos = 0

    def __repr__(self):
        return f'(ID: {self.index}; type: {self.type})'
    
    def __str__(self):
        return f'(ID: {self.index}; type: {self.type})'

    def add_time(self,time):
        self.current_time += time

    def deliver_pallets(self, delivered, vertex, distance):
        time = distance/self.speed
        self.add_time(time)
        self.current_capacity -= delivered
        self.current_pos = vertex

    def refill(self, distance_to_base):
        time = distance_to_base/self.speed
        self.add_time(time)
        self.current_capacity = self.capacity
        self.current_pos = 0


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
                #TODO: zmiana diagonalnych wartośći na odległość od bazy
                self.matrix[i][i] = 10
