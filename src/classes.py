#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from random import randint
from random import choice
from enum import Enum
from typing import List


class TruckType(Enum):
    SMALL = "SMALL"
    LARGE = "LARGE"


class Order:
    unique = 0
    simulation_time = None

    def __init__(
        self,
        graph=None,
        n_pallets: int = None,
        max_pallets: int = 10,
        vertex: int = None,
        deadline: int = None,
        index: int = None,
    ):
        if index is None:
            self.index = self.unique
            self.__class__.unique += 1
        else:
            self.index = index
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
        if deadline is None:
            self.deadline = randint(1, self.__class__.simulation_time)
        else:
            self.deadline = deadline

    def __repr__(self):
        return f"(id={self.index}, v={self.vertex}, n_p={self.n_pallets}, dl={self.deadline})"

    def __str__(self):
        return f"(id={self.index}, destination_idx={self.vertex}, number_of_pallets={self.n_pallets}, deadline={self.deadline})"

    @classmethod
    def reset_id(cls):
        cls.unique = 0


class SolutionTuple:
    def __init__(self, n_order, n_pallets):
        self.n_order = n_order
        self.n_pallets = n_pallets

    def __repr__(self):
        return f"({self.n_order}, {self.n_pallets})"

    def __str__(self):
        return f"({self.n_order}, {self.n_pallets})"


class Truck:
    unique = 0
    small_speed = None
    small_capacity = None
    large_speed = None
    large_capacity = None

    def __init__(self, truck_type, index: int = None):
        if isinstance(truck_type, TruckType):
            self.type = truck_type
        else:
            if truck_type == "TruckType.SMALL":
                self.type = TruckType.SMALL
            elif truck_type == "TruckType.LARGE":
                self.type = TruckType.LARGE
            else:
                raise TypeError("Invalid truck type.")

        if index is None:
            self.index = self.unique
            self.__class__.unique += 1
        else:
            self.index = index

        if self.type == TruckType.SMALL:
            self.speed = self.__class__.small_speed
            self.capacity = self.__class__.small_capacity
        elif self.type == TruckType.LARGE:
            self.speed = self.__class__.large_speed
            self.capacity = self.__class__.large_capacity

        self.current_time = 0
        self.current_capacity = self.capacity
        self.current_pos = -1

    def __repr__(self):
        return f"(ID: {self.index}; type: {self.type})"

    def __str__(self):
        return f"(ID: {self.index}; type: {self.type})"

    def add_time(self, time):
        self.current_time += time

    def deliver_pallets(self, delivered, vertex, distance):
        time = distance / self.speed
        self.add_time(time)
        self.current_capacity -= delivered
        self.current_pos = vertex

    def refill(self, distance_to_base):
        time = distance_to_base / self.speed
        self.add_time(time)
        self.current_capacity = self.capacity
        self.current_pos = -1

    @classmethod
    def reset_id(cls):
        cls.unique = 0


class Graph:
    def __init__(self, rows=None, cols=None, matrix=None):
        if rows is None:
            self.rows = len(matrix)
        else:
            self.rows = rows

        if rows is None:
            self.cols = len(matrix[0])
        else:
            self.cols = cols
        self.matrix = np.array(matrix)
        self.list_of_vertices = [i for i in range(self.rows)]
        self.min_values = []

    def __repr__(self):
        return self.matrix

    def __str__(self):
        return "{}".format(self.matrix)

    def create_adj_matrix(self, low_value, high_value):
        if self.matrix is None:
            weighted_matrix = np.random.randint(high=high_value, size=(self.rows, self.cols), low=low_value)
            self.matrix = np.maximum(weighted_matrix, weighted_matrix.transpose())

            for i in range(self.rows):
                self.matrix[i][i] = high_value

            for i in range(self.rows):
                self.min_values.append(np.min(self.matrix[i]))

            for i in range(self.rows):
                # zmiana diagonalnych wartośći na odległość od bazy
                # - przyjmuje, że odległość do bazy jest równa minimalnej
                # odległości w danym wierszu/kolumnie - nie ma róźnicy,
                # które przyjmiemy bo macierz jest symetryczna.
                self.matrix[i][i] = self.min_values[i]

    def print_min_to_check(self):
        print("Wartości minimalne po wierszach: {}".format(self.min_values))


CompleteSolution = List[List[SolutionTuple]]
