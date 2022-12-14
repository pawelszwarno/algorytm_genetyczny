from classes import Order, Truck, SolutionTuple, Graph, TruckType
from typing import List
from random import randint, choice, shuffle, random
from variables import penalty_factor, n_small_trucks, n_large_trucks

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


# funkcja mutacji wariant 1: zamiana kolejności w trasie losowej ilości ciężarówek 
def mutation(new_sol: List[List[SolutionTuple]], truck_list: List[Truck], r_mut = 1.0):
    rand_float = random()
    # jesli prawdopodobieństwo niższe niż threshold to zwracamy bez zmian
    if rand_float > r_mut:
        return new_sol
    else:
        # jesli ma dojsc do mutacji to losujemy liczbe od 1 do maks liczby ciężarówek
        n_of_trucks_to_mut = randint(1, len(truck_list))
        # print("DO MUTACJI {}".format(n_of_trucks_to_mut))
        new_truck_list = truck_list.copy()
        shuffle(new_truck_list)
        # bierzemy tylko n_of_trucks_to_mut z losowych tras ciężarówek
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

def create_structures(rows_cols: int, low_adj_matrix, high_adj_matrix: float, n_of_orders: int):
    # stworzenie grafu:
    g = Graph(rows_cols, rows_cols)
    g.create_adj_matrix(low_adj_matrix, high_adj_matrix)
    # print("Macierz sąsiedztwa: ")
    # print(g, '\n')
    
    # stworzenie listy ciężarówek:
    trucks_list = [Truck(TruckType.SMALL) for _ in range(n_small_trucks)]
    for _ in range(n_large_trucks):
        trucks_list.append(Truck(TruckType.LARGE))
    # print("Lista ciężarówek: (Index, typ)")
    # print(trucks_list, '\n')
    
    # Stworzenie listy zleceń złożonej z instancji klasy Order z polami:
    # deadline - czyli czas w którym trzeba dostarczyć dostawę i * 1000 (wyrażany w minutach np.)
    orders_lst = [Order(g, 20) for _ in range(n_of_orders)]
    # print("Lista zleceń: ")
    # print(orders_lst, '\n')
    # lista zleceń, liczba dużych ciężarówek, liczba małych ciężarówek,
    # pojemność małych ciężarówek, pojemność dużych ciężarówek
    return g, trucks_list, orders_lst
    
    
def algorithm(n_population: int, n_iteration: int , r_cross: float, r_mutation: float, truck_list: List[Truck], order_lst: List[Order], g: Graph):
    children = []
    population = generate_solution(truck_list, order_lst, n_large_trucks, n_small_trucks)
    best, best_eval = population, objective_function(population, g, truck_list, order_lst)
    for generation in range(n_iteration):
        scores = [objective_function(child, g, truck_list, order_lst) for child in population]
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


