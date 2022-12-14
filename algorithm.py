from classes import Order, Truck, SolutionTuple, Graph
from typing import List
from random import randint, choice, shuffle, random
from variables import penalty_factor


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

# funkcja mutacji wariant 1: zamiana kolejno??ci w trasie losowej ilo??ci ci????ar??wek 
def mutation(new_sol: List[List[SolutionTuple]], truck_list: List[Truck], r_mut = 1.0):
    rand_float = random()
    # jesli prawdopodobie??stwo ni??sze ni?? threshold to zwracamy bez zmian
    if rand_float > r_mut:
        return new_sol
    else:
        # jesli ma dojsc do mutacji to losujemy liczbe od 1 do maks liczby ci????ar??wek
        n_of_trucks_to_mut = randint(1, len(truck_list))
        # print("DO MUTACJI {}".format(n_of_trucks_to_mut))
        new_truck_list = truck_list.copy()
        shuffle(new_truck_list)
        # bierzemy tylko n_of_trucks_to_mut z losowych tras ci????ar??wek
        for i in range(n_of_trucks_to_mut):
            truck_id_to_mut = new_truck_list[i].index
            left_swap = randint(0, len(new_sol[truck_id_to_mut]) - 1)
            right_swap = randint(0, len(new_sol[truck_id_to_mut]) - 1)
            temp = new_sol[truck_id_to_mut][left_swap]
            new_sol[truck_id_to_mut][left_swap] = new_sol[truck_id_to_mut][right_swap]
            new_sol[truck_id_to_mut][right_swap] = temp
        return new_sol
            
            
            

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


def algorithm():
    pass