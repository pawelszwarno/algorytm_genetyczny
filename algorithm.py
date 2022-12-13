from classes import Order, Truck, SolutionTuple
from typing import List
from random import randint
from random import choice


# TO DO
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


def objective_function(solution):
    pass


def mutation():
    pass


def crossing():
    pass


def algorithm():
    pass