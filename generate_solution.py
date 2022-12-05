#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint
from typing import List

class Order:
    unique = 0

    def __init__(self,n_pallets, vertex,deadline):
        self.index = self.unique
        self.n_pallets = n_pallets
        self.vertex = vertex
        self.deadline = deadline
        self.__class__.unique += 1

    def __repr__(self):
        return f'(index={self.index}, n_pallets={self.n_pallets})'

    def __str__(self):
        return f'(index={self.index}, n_pallets={self.n_pallets})'


class SolutionTuple:
    def __init__(self,n_order,n_pallets):
        self.n_order = n_order
        self.n_pallets = n_pallets

    def __repr__(self):
        return f'({self.n_order}, {self.n_pallets})'

    def __str__(self):
        return f'({self.n_order}, {self.n_pallets})'


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

def main():
    orders_lst = [Order(i+2, i % 15, i*1000) for i in range(30)]
    print("Order list:")
    print(orders_lst)
    print()
    sol = generate_solution(orders_lst, 3,5,4,7)
    for lst in sol:
        print(lst)

main()