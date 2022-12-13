from classes import Order, Truck, SolutionTuple, Graph, TruckType
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
                curr_truck = truck_list[truck_idx]
                distance = cost_graph.matrix[curr_order.n_order, prev_order.n_order]
                time = distance/curr_truck.speed
                curr_truck.add_time(time)
                delivery_time = curr_truck.current_time

                delivered_pallets = min(curr_truck.current_capacity, curr_order.n_pallets)
                order_list[curr_order.n_order].deliver_pallets(delivered_pallets)
                curr_order.n_pallets -= delivered_pallets
                curr_truck.deliver_pallets(delivered_pallets)

                if delivery_time > order_list[curr_order.n_order].deadline:
                    penalty = penalty_factor * (delivery_time - order_list[curr_order.n_order].deadline) * (order_list[curr_order.n_order].missing_pallets + delivered_pallets)
                    cost += penalty

                if curr_truck.current_capacity == 0:
                    curr_truck.refill(distance_to_base=cost_graph.matrix[curr_order.n_order, 0])

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


# stworzenie grafu:
g = Graph(6, 6)
g.create_adj_matrix(0, 10)
# print("Macierz sąsiedztwa: ")
# print(g, '\n')

# stworzenie listy ciężarówek:
n_small_trucks = 7
n_large_trucks = 6
trucks_list = [Truck(TruckType.SMALL) for _ in range(n_small_trucks)]
for _ in range(n_large_trucks):
    trucks_list.append(Truck(TruckType.LARGE))
# print("Lista ciężarówek: (Index, typ)")
# print(trucks_list, '\n')

# Stworzenie listy zleceń złożonej z instancji klasy Order z polami:
# deadline - czyli czas w którym trzeba dostarczyć dostawę i * 1000 (wyrażany w minutach np.)
orders_lst = [Order(g, 20) for i in range(20)]
# print("Lista zleceń: ")
# print(orders_lst, '\n')
# lista zleceń, liczba dużych ciężarówek, liczba małych ciężarówek,
# pojemność małych ciężarówek, pojemność dużych ciężarówek

def algorithm(n_population: int, n_iteration: int , r_cross: float, r_mutation: float):
    children = []
    population = generate_solution(trucks_list, orders_lst, n_large_trucks, n_small_trucks)
    best, best_eval = 0, objective_function(population[0], g, trucks_list, orders_lst)
    for generation in range(n_iteration):
        scores = [objective_function(child, g, trucks_list, orders_lst) for child in population]
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

def selection_rank(population, scores, n_population):
    sel_lst = []
    
    for ix in range(len(population)):
        if len(sel_lst) == 0:
            sel_lst.append((population[ix],scores[ix]))

        if scores[ix] > sel_lst[-1][1]:
            if len(sel_lst) >= n_population:
                sel_lst[-1] = (population[ix],scores[ix])
            elif len(sel_lst) < n_population:
                sel_lst.append((population[ix],scores[ix]))
        sel_lst.sort(reverse = 1, key = lambda x: x[1])
    
    return sel_lst

# popi = [1,2,3,4,5,6,((1,3),(2,1),(5,1),(6,2),(8,4)),8,9,10,12,16]
# scor = [1,2,3,4,5,6,7,8,9,10,12,16]
# lens = 10
# print(selection_rank(popi, scor, lens))

# print(generate_solution(trucks_list, orders_lst, n_large_trucks, n_small_trucks))
print(algorithm(n_population, n_iteration, r_cross, r_mutation))