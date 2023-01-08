from src.classes import Order, Truck, SolutionTuple, Graph, TruckType, CompleteSolution
from typing import List
from random import randint, choice, shuffle, random, sample, randrange
from src import variables
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np


def generate_solution(trucks_list: List[Truck], orders_list: List[Order], n_large_truck: int, n_small_truck: int) -> List[CompleteSolution]:
    population = []
    for _ in range(variables["algorithm_data"]['n_pop']):
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
        population.append(solution)
    return population


def objective_function(solution: CompleteSolution, cost_graph: Graph, truck_list: List[Truck], order_list: List[Order], uncomplete_sol: bool=True):
    cost = 0
    for j in truck_list:
        j.current_capacity = j.capacity
        j.current_time = 0
        j.current_pos = 0
    if uncomplete_sol:
        delivered_pallets_in_order = [0 for _ in range(len(order_list))]
    for truck_idx, truck_route in enumerate(solution):
        prev_order_nr = None
        curr_truck = truck_list[truck_idx]
        for curr_order in truck_route:
            curr_order_info = order_list[curr_order.n_order]
            missing_pallets = curr_order.n_pallets
            while missing_pallets > 0:

                if prev_order_nr is None:
                    distance = cost_graph.matrix[curr_order_info.vertex, curr_order_info.vertex]
                else:
                    distance = cost_graph.matrix[curr_order_info.vertex, order_list[prev_order_nr].vertex]

                delivered_pallets = min(curr_truck.current_capacity, missing_pallets)
                missing_pallets -= delivered_pallets
                if uncomplete_sol:
                    delivered_pallets_in_order[curr_order.n_order] += delivered_pallets
                
                curr_truck.deliver_pallets(delivered_pallets, curr_order_info.vertex, distance)
                delivery_time = curr_truck.current_time
                # if delivery_time <= curr_order_info.deadline:
                #     print("Zamówienie dowiezione na czas")
                
                if delivery_time > curr_order_info.deadline:
                    penalty = variables["algorithm_data"]['penalty_factor'] * (delivery_time - curr_order_info.deadline) * (delivered_pallets)
                    # print("Deadline: {}".format(curr_order_info.deadline))
                    # print("Czas dowozu: {}".format(delivery_time))
                    # print("Kara jest równa {}".format(penalty))
                    cost += penalty

                if curr_truck.current_capacity == 0:
                    curr_truck.refill(distance_to_base=cost_graph.matrix[curr_truck.current_pos, curr_truck.current_pos])

                prev_order_nr = curr_order.n_order
    
    if uncomplete_sol:
        for idx, pallets in enumerate(delivered_pallets_in_order):
            if order_list[idx].n_pallets > pallets:
                penalty = variables["algorithm_data"]['penalty_factor']*0.1 * variables["structures_data"]['SIMULATION_TIME'] * (order_list[idx].n_pallets - pallets)
                cost += penalty
                
    return int(cost)


# funkcja mutacji wariant 1: zamiana kolejności w trasie losowej ilości ciężarówek 
def mutation(new_sol: CompleteSolution, truck_list: List[Truck], r_mut = 1.0):
    rand_float = random()
    # jesli prawdopodobieństwo niższe niż threshold to zwracamy bez zmian
    if rand_float > r_mut:
        return new_sol
    else:
        # jesli ma dojsc do mutacji to losujemy liczbe od 1 do maks liczby ciężarówek
        n_of_trucks_to_mut = randint(1, len(truck_list)//2)
        # print("DO MUTACJI {}".format(n_of_trucks_to_mut))
        new_truck_list = deepcopy(truck_list)
        shuffle(new_truck_list)
        # bierzemy tylko n_of_trucks_to_mut z losowych tras ciężarówek
        for i in range(n_of_trucks_to_mut):
            truck_id_to_mut = new_truck_list[i].index
            if len(new_sol[truck_id_to_mut]) - 1 < 1:
                continue
            else:
                left_swap = randint(0, len(new_sol[truck_id_to_mut])-1)
                right_swap = randint(0, len(new_sol[truck_id_to_mut])-1)
                temp = new_sol[truck_id_to_mut][left_swap]
                new_sol[truck_id_to_mut][left_swap] = new_sol[truck_id_to_mut][right_swap]
                new_sol[truck_id_to_mut][right_swap] = temp
        return new_sol


def crossing_with_possibly_uncomplete(parent_1: CompleteSolution, parent_2: CompleteSolution):
    new_sol = [[] for _ in range(len(parent_1))]
    r_cross = randrange(variables["structures_data"]["n_of_orders"])
    for idx, truck_route in enumerate(parent_1):
        for idx_2, sol in enumerate(truck_route):
            if idx_2 < r_cross:
                new_sol[idx].append(sol)
            else:
                break

    for idx, truck_route in enumerate(parent_2):
        for idx_2, sol in enumerate(truck_route):
            if idx_2 < r_cross:
                continue
            else:
                new_sol[idx].append(sol)
    return new_sol
    

def crossing(parent_1: CompleteSolution, parent_2: CompleteSolution, possibly_uncomplete: bool=False):
    if possibly_uncomplete:
        return crossing_with_possibly_uncomplete(parent_1, parent_2)
    new_sol = [[] for _ in range(len(parent_1))]
    r_cross = randrange(variables["structures_data"]["n_of_orders"])
    for idx, truck_route in enumerate(parent_1):
        for sol in truck_route:
            if sol.n_order < r_cross:
                new_sol[idx].append(sol)
            else:
                continue

    for idx, truck_route in enumerate(parent_2):
        for sol in truck_route:
            if sol.n_order < r_cross:
                continue
            else:
                new_sol[idx].append(sol)
    return new_sol


# funkcja do stworzenia grafu, listy ciężarówek i listy zleceń:
def create_structures(rows_cols, low_adj_matrix, high_adj_matrix, n_of_orders, max_pallets):
    # graf:
    Order.reset_id()
    Truck.reset_id()
    g = Graph(rows_cols, rows_cols)
    g.create_adj_matrix(low_adj_matrix, high_adj_matrix)
    # lista ciężarówek:
    trucks_list = [Truck(TruckType.SMALL) for _ in range(variables["structures_data"]['n_small_trucks'])]
    for _ in range(variables["structures_data"]['n_large_trucks']):
        trucks_list.append(Truck(TruckType.LARGE))
    # lista zleceń:
    orders_lst = [Order(g, max_pallets=max_pallets) for _ in range(n_of_orders)]
    Order.reset_id()
    Truck.reset_id()
    return g, trucks_list, orders_lst

 
# selekcja najprostsza ze wszystkich - rankingowa
def selection(population_scores: List[tuple[int, int]], population_size: int):
    population_scores.sort(key = lambda x: x[1])
    selected = population_scores[0:population_size]
    return selected


def selection_rank(population_score: List[tuple[int, int]] = None, population_size: int =None):

    if len(population_score) < population_size:
        raise ValueError

    selected = []
    population_score.sort(key = lambda x: x[1], reverse=1)
    pop_rank = np.zeros(len(population_score)+1) 

    for i in range(len(population_score)):
        j = len(population_score) - i 
        pop_rank[i] = j**2
    
    while len(selected) != population_size:

        select = randint(1, pop_rank[0]+1)
        temp = False

        for i in range(len(population_score)):
            if temp == True:
                pass
            
            if temp == False:
                if select <= pop_rank[i] and select > pop_rank[i+1]:
                    if population_score[i] in selected:
                        break
                    if population_score[i] not in selected:
                        selected.append(population_score[i])
                        temp = True
    
    return selected



# moja (PSu) implementacja ruletki
def selection_roulette(population_scores: List[tuple[int, int]], population_size: int):
    scores = np.array([score for _, score in population_scores])
    total_score = scores.sum()
    probabilities = scores / total_score
    indices = np.arange(len(population_scores))
    selected_indices = np.random.choice(indices, size=population_size, p=probabilities, replace=False)
    return [population_scores[i] for i in selected_indices]


# moja (PSu) implementacja turniejowego
def selection_tour(population_scores: List[tuple[int, int]], population_size: int):
    selected = []
    population = [item[0] for item in population_scores]
    while len(selected) < population_size:
        tour = sample(population, min(3, len(population)))
        tour_scores = [(index, score) for index, score in population_scores if index in tour]
        tour_scores.sort(key = lambda x: x[1], reverse = True)
        winner = tour_scores[0]
        selected.append(winner)
        population.remove(winner[0])
    return selected


def algorithm(n_iteration: int, r_mutation: float, truck_list: List[Truck], order_lst: List[Order], g: Graph, selection_function: callable, uncomplete_sol: bool):
    population = generate_solution(truck_list, order_lst, variables["structures_data"]['n_large_trucks'], variables["structures_data"]['n_small_trucks'])
    best_eval_list = []
    iteration_eval_list = []
    best = population[0]
    best_eval = objective_function(population[0], g, truck_list, order_lst, False)
    best_eval_list.append(best_eval)
    iteration_eval_list.append(best_eval)
    print("Najlepsze rozwiązanie w pierwszej iteracji: ")
    print(best)
    print("Wartość funkcji celu w pierwszej iteracji:")
    print(best_eval)
    for _ in range(n_iteration):
        children = []
        population_scores = []
        for i in range(variables["algorithm_data"]['n_pop']):
            cost = objective_function(population[i], g, truck_list, order_lst)
            population_scores.append((i, cost))
        selected = selection_function(population_scores, variables["algorithm_data"]['n_pop'])
        
        # nadpisanie najlepszego rozwiązania i best_eval JEŚLI obecna najmniejsza wart. funkcji celu jest większa:
        if population_scores[0][1] < best_eval:
            best_eval = population_scores[0][1]
            best = population[selected[0][0]]
        
        # dodanie do list, z których później będzie robiony wykres:
        best_eval_list.append(best_eval)
        iteration_eval_list.append(population_scores[0][1])
        
        for i in range(0, len(selected)-1, 2):
            parent_1, parent_2 = population[selected[i][0]], population[selected[i+1][0]]
            child = crossing(parent_1, parent_2, possibly_uncomplete=uncomplete_sol)
            new_child = mutation(child, truck_list, r_mutation)
            children.append(new_child)
            # child2 = crossing(parent_1, parent_2, r_mutation)
            # children.append(child2)
            children.append(choice([parent_1, parent_2]))
        print(best_eval)
        population = children
        
    return best, best_eval, best_eval_list, iteration_eval_list


def visualise(best_eval_list, iteration_eval_list):
    plt.figure()
    plt.plot(best_eval_list, label='Najlepsza wartość funkcji celu')
    plt.plot(iteration_eval_list, label='Wartość funkcji celu w danej iteracji')
    plt.title('Wykres zależności funkcji celu do iteracji')
    plt.xlabel('Nr iteracji')
    plt.ylabel('Wartość funkcji celu')
    plt.tight_layout() 
    plt.savefig('data/wykres_funkcji_celu.png', dpi = 100)