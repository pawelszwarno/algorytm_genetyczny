#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from random import randint
from random import choice
from typing import List

class Order:
    unique = 0

    # 30 dni - 30*24 = 720h
    # deadline dany jako losowa liczba godzin od czasu startwoego 0:
    # czyli np. deadline 32 znaczy 1 dzień i 8h po rozpoczęciu mięsiąca 
    # naszego horyzontu czasowego.
    # zmieniłem, że bierze losowy wierzchołek z grafu,
    # i losową liczbę palet od 1 do max_liczby
    def __init__(self, graph, max_pallets):
        self.index = self.unique
        self.n_pallets = randint(1, max_pallets)
        self.vertex = choice(graph.list_of_vertices)
        self.deadline = randint(1, 720)
        self.__class__.unique += 1

    def __repr__(self):
        return f'(id={self.index}, v={self.vertex}, n_p={self.n_pallets})'

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
    
    def __init__(self, type):
        self.type = type
        self.index = self.unique
        if type == 'small':
            self.speed = 5
            self.capacity = 4
        elif type == 'large':
            self.speed = 3
            self.capacity = 7
        self.__class__.unique += 1
        
    def __repr__(self):
        return f'(ID: {self.index}; type: {self.type})'
    
    def __str__(self):
        return f'(ID: {self.index}; type: {self.type})'
    

def generate_solution(trucks_list: List[Truck], orders_list: List[Order], n_large_truck: int, n_small_truck: int, capacity_small: int, capacity_large: int) -> List[List[SolutionTuple]]:
    solution = [[] for _ in range(n_large_truck+n_small_truck)]
    for order in orders_list:
        current_n_pallets = order.n_pallets
        while current_n_pallets > 0:
            hired_truck = random.choice(trucks_list)
            n_pallets = randint(1, min(current_n_pallets, hired_truck.capacity))
            solution[hired_truck.index].append(SolutionTuple(order.index, n_pallets))
            current_n_pallets -= n_pallets
    return solution