from classes import Order, Truck, SolutionTuple, Graph
from typing import List
from random import randint
from random import choice
from variables import penalty_factor, n_population, n_iteration, r_cross, r_mutation


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


def objective_function(solution: List[List[SolutionTuple]], cost_graph: Graph, truck_list: List[Truck], order_list: List[Order]):
    cost = 0
    for truck_idx, truck_route in enumerate(solution):
        prev_order = truck_route[0]
        for curr_order in truck_route:
            while curr_order.n_pallets > 0:
                distance = cost_graph.matrix[curr_order.n_order, prev_order.n_order]
                time = distance/truck_list[truck_idx].speed
                truck_list[truck_idx].add_time(time)
                delivery_time = truck_list[truck_idx].current_time
                if delivery_time > order_list[curr_order.n_order].deadline:
                    penalty = penalty_factor * (delivery_time - order_list[curr_order.n_order].deadline)
                    cost += penalty
                prev_order = curr_order
    return cost


def mutation():
    pass


def crossing(parent_1: List[List[SolutionTuple]], parent_2: List[List[SolutionTuple]], r_cross: int):
    new_sol = [[] for _ in range(len(parent_1))]
    for idx, truck_route in enumerate(parent_1):
        for sol in truck_route:
            if sol.n_order < r_cross:
                new_sol[idx].append(sol)
            else:
                break

    for idx, truck_route in enumerate(parent_2):
        for sol in truck_route:
            if sol.n_order < r_cross:
                continue
            else:
                new_sol[idx].append(sol)
    return new_sol


def algorithm(n_population: int, n_iteration: int , r_cross: float, r_mutation: float):
    children = []
    population = generate_solution()
    best, best_eval = 0, objective_function(population[0])
    for generation in range(n_iteration):
        scores = [objective_function(c) for c in population]
        for i in range(n_population):
            if scores[i] < best_eval:
                best, best_eval = population[i], scores[i]
        selected = selection_rank(population, scores)
        for i in range(0, n_population, 2):
            parent_1, parent_2 = selected[i], selected[i+1]
            for child in crossing(parent_1, parent_2, r_cross):
                mutation(child, r_mutation)
                children.append(child)
        population = children
    return best, best_eval

def selection_rank(population, scores):

    pass