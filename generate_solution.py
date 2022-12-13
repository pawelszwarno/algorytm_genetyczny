#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint
from random import choice
from typing import List
from enum import Enum
SIMULATION_TIME = 720  # 30 dni - 30*24 = 720h


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
        self.deadline = randint(1, SIMULATION_TIME)
        self.__class__.unique += 1

    def __repr__(self):
        return f'(id={self.index}, v={self.vertex}, n_p={self.n_pallets}, dl={self.deadline})'

    def __str__(self):
        return f'(id={self.index}, v={self.vertex}, n_p={self.n_pallets})'


class SolutionTuple:
    def __init__(self,n_order,n_pallets):
        self.n_order = n_order
        self.n_pallets = n_pallets

    def __repr__(self):
        return f'({self.n_order}, {self.n_pallets})'

    def __str__(self):
        return f'({self.n_order}, {self.n_pallets})'


class Truck:
    unique = 0
    
    def __init__(self, type: TruckType):
        self.type = type
        self.index = self.unique
        if type == TruckType.SMALL:
            self.speed = 5
            self.capacity = 4
        elif type == TruckType.LARGE:
            self.speed = 3
            self.capacity = 7
        self.__class__.unique += 1

    def __repr__(self):
        return f'(ID: {self.index}; type: {self.type})'
    
    def __str__(self):
        return f'(ID: {self.index}; type: {self.type})'
    

def generate_solution(trucks_list: List[Truck], orders_list: List[Order], n_large_truck: int, n_small_truck: int) -> List[List[SolutionTuple]]:
    solution = [[] for _ in range(n_large_truck+n_small_truck)]
    for order in orders_list:
        current_n_pallets = order.n_pallets
        while current_n_pallets > 0:
            hired_truck = choice(trucks_list)
            n_pallets = randint(1, current_n_pallets)
            if solution[hired_truck.index]:
                last_order = solution[hired_truck.index][-1]
                if last_order.n_order == order.index:
                    solution[hired_truck.index][-1] = SolutionTuple(order.index, n_pallets+last_order.n_pallets)
                else:
                    solution[hired_truck.index].append(SolutionTuple(order.index, n_pallets))
            else:
                solution[hired_truck.index].append(SolutionTuple(order.index, n_pallets))
            current_n_pallets -= n_pallets
    return solution
