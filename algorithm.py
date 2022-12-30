from classes import Order, Truck, SolutionTuple, Graph, TruckType, SelectionType
from typing import List
from random import randint, choice, shuffle, random
from variables import penalty_factor, n_small_trucks, n_large_trucks, n_pop, SIMULATION_TIME, parent_percent
from copy import deepcopy
    
   
def generate_solution(trucks_list: List[Truck], orders_list: List[Order], n_large_truck: int, n_small_truck: int) -> List[List[List[SolutionTuple]]]:
    population = []
    for _ in range(n_pop):
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


def objective_function(solution: List[List[SolutionTuple]], cost_graph: Graph, truck_list: List[Truck], order_list: List[Order], uncomplete_sol=True):
    cost = 0
    for j in truck_list:
                j.current_capacity = j.capacity
                j.current_time = 0
                j.current_pos = 0
    if uncomplete_sol:
        delivered_pallets_in_order = [0 for _ in range(len(order_list))]
    for truck_idx, truck_route in enumerate(solution):
        prev_order_nr = None
        for curr_order in truck_route:
            curr_order_info = order_list[curr_order.n_order]
            missing_pallets = curr_order.n_pallets
            while missing_pallets > 0:

                curr_truck = truck_list[truck_idx]
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
                    penalty = penalty_factor * (delivery_time - curr_order_info.deadline) * (delivered_pallets)
                    # print("Deadline: {}".format(curr_order_info.deadline))
                    # print("Czas dowozu: {}".format(delivery_time))
                    # print("Kara jest równa {}".format(penalty))
                    cost += penalty

                if curr_truck.current_capacity == 0:
                    curr_truck.refill(distance_to_base=cost_graph.matrix[curr_truck.current_pos, curr_truck.current_pos])

                prev_order_nr = curr_order.n_order
    
    if uncomplete_sol:
        for idx, pallets in enumerate(delivered_pallets_in_order):
            penalty = penalty_factor*10 * SIMULATION_TIME * (order_list[idx].n_pallets - pallets)
            cost += penalty
                
    return int(cost)


# funkcja mutacji wariant 1: zamiana kolejności w trasie losowej ilości ciężarówek 
def mutation(new_sol: List[List[SolutionTuple]], truck_list: List[Truck], r_mut = 1.0):
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


def crossing_with_possibly_uncomplete(parent_1: List[List[SolutionTuple]], parent_2: List[List[SolutionTuple]], r_cross: int, possibly_uncomplete: bool=False):
    new_sol = [[] for _ in range(len(parent_1))]
    for idx, truck_route in enumerate(parent_1):
        for idx_2, sol in enumerate(truck_route):
            if idx_2 < r_cross:
                new_sol[idx].append(sol)
            else:
                break

    for idx, truck_route in enumerate(parent_2):
        for idx_2, sol in enumerate(truck_route):
            if sol.n_order < r_cross:
                continue
            else:
                new_sol[idx].append(sol)
    return new_sol
    

def crossing(parent_1: List[List[SolutionTuple]], parent_2: List[List[SolutionTuple]], r_cross: int, possibly_uncomplete: bool=False):
    if possibly_uncomplete:
        return crossing_with_possibly_uncomplete(parent_1, parent_2, r_cross)
    new_sol = [[] for _ in range(len(parent_1))]
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
def create_structures(rows_cols: int, low_adj_matrix, high_adj_matrix: float, n_of_orders: int):
    # graf:
    g = Graph(rows_cols, rows_cols)
    g.create_adj_matrix(low_adj_matrix, high_adj_matrix)
    # lista ciężarówek:
    trucks_list = [Truck(TruckType.SMALL) for _ in range(n_small_trucks)]
    for _ in range(n_large_trucks):
        trucks_list.append(Truck(TruckType.LARGE))
    # lista zleceń:
    orders_lst = [Order(g, 7) for _ in range(n_of_orders)]
    return g, trucks_list, orders_lst

 
# selekcja najprostsza ze wszystkich - rankingowa
def selection(population_scores: List[tuple[int, int]], population_size: int):
    population_scores.sort(key = lambda x: x[1])
    selected = population_scores[0:population_size]
    return selected


# selekcja tournament:
def selection_tour(population_score: List[tuple[int, int]] = None, population_size: int =None):
    selected = []
    if len(population_score) < population_size:
        raise ValueError
    if (len(population_score)%2) != 0:  
        selected.append(population_score[len(population_score)%2])
    for i in range(int(len(population_score)/2)):
        if population_score[i][1] >= population_score[-1-i][1]:
            selected.append(population_score[i])
        elif population_score[i][1] <= population_score[-1-i][1]:
            selected.append(population_score[-1-i])
    if len(selected) < population_size:
        pass
    elif len(selected) == population_size:
        return selected
    elif len(selected) > population_size:
        return selection_tour(selected, population_size)


# selekcja - ruletka
def selection_prop(population_score: List[tuple[int, int]] = None, population_size: int =None):

    selected = []
    pop_edited = [population_score[0]]
    
    if len(population_score) < population_size:
        raise ValueError

    for i in range(1,len(population_score)):
        temp = pop_edited[i-1][1] + population_score[i][1]
        pop_edited.append((population_score[i][0], temp))
    
    while len(selected) != population_size:
        select = randint(1, pop_edited[-1][1])

        for i in range(len(pop_edited)):
            if select <= pop_edited[i][1]:
                if population_score[i] not in selected:
                    selected.append(population_score[i])
        return selected


# AKTUALNIE ALGORYTM DZIAŁA w następujący sposób:
# są do wyboru 3 selection_type wybierane przy wywołaniu (ruletka do napisania, ranking na pewno działa poprawnie, nwm jak touranment)
# n_pop - globalna zmienna z variables decyduje o wielkości populacji
# do następnego pokolenia brany jest jeden z rodziców z równą szansą
def algorithm(n_iteration: int , r_cross: float, r_mutation: float, truck_list: List[Truck], order_lst: List[Order], g: Graph, selection_function, uncomplete_sol):
    population = generate_solution(truck_list, order_lst, n_large_trucks, n_small_trucks)
    best = population[0]
    best_eval = objective_function(population[0], g, truck_list, order_lst, uncomplete_sol)
    print("Najlepsze rozwiązanie w pierwszej iteracji: ")
    print(best)
    print("Wartość funkcji celu w pierwszej iteracji:")
    print(best_eval)
    for _ in range(n_iteration):
        children = []
        population_scores = []
        for i in range(n_pop):
            cost = objective_function(population[i], g, truck_list, order_lst)
            population_scores.append((i, cost))

        selected = selection_function(population_scores, n_pop)
            
        # nadpisanie najlepszego rozwiązania i best_eval JEŚLI obecna najmniejsza wart. funkcji celu jest większa:
        if population_scores[0][1] < best_eval:
            best_eval = population_scores[0][1]
            best = population[selected[0][0]]
        
        for i in range(0, len(selected)-1, 2):
            parent_1, parent_2 = population[selected[i][0]], population[selected[i+1][0]]
            child = crossing(parent_1, parent_2, r_cross, possibly_uncomplete=False)
            new_child = mutation(child, truck_list, r_mutation)
            children.append(new_child)
            # child2 = crossing(parent_1, parent_2, r_mutation)
            # children.append(child2)
            children.append(choice([parent_1, parent_2]))
        print(best_eval)
        population = children
    return best, best_eval


