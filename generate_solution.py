#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint
from typing import List

class Order:
    unique = 0

    def __init__(self,n_pallets):
        self.index = self.unique
        self.n_pallets = n_pallets
        self.__class__.unique += 1

class SolutionTuple:
    def __init__(self,n_order,n_pallets):
        self.n_order = n_order
        self.n_pallets = n_pallets


def generate_solution(orders_list: List[Order], n_large_truck: int, n_small_truck: int, capacity_small: int, capacity_large: int) -> List[List[SolutionTuple]]:
    solution = [[] for _ in range(n_large_truck+n_small_truck)]
    for order in orders_list:
        current_n_pallets = order.n_pallets
        while current_n_pallets > 0:
            hired_truck = randint(0,n_large_truck+n_small_truck-1)
            if hired_truck < n_small_truck:
                n_pallets = randint(1,min(current_n_pallets,capacity_small))
            else:
                n_pallets = randint(1, min(current_n_pallets, capacity_large))
            solution[hired_truck].append(SolutionTuple(order.index, n_pallets))
            current_n_pallets -= n_pallets
    return solution