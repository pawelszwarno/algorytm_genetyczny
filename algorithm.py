from classes import Order, Truck, SolutionTuple, Graph, TruckType
from typing import List
from random import randint, choice, shuffle, random
from variables import penalty_factor, n_small_trucks, n_large_trucks, n_pop, SIMULATION_TIME, parent_percent
from copy import deepcopy

# TO DO
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

                if delivery_time > curr_order_info.deadline:
                    penalty = penalty_factor * (delivery_time - curr_order_info.deadline) * (delivered_pallets)
                    cost += penalty

                if curr_truck.current_capacity == 0:
                    curr_truck.refill(distance_to_base=cost_graph.matrix[curr_truck.current_pos, curr_truck.current_pos])

                prev_order_nr = curr_order.n_order
    
    if uncomplete_sol:
        for idx, pallets in enumerate(delivered_pallets_in_order):
            penalty = penalty_factor*10 * SIMULATION_TIME * (order_list[idx].n_pallets - pallets)
            cost += penalty
                
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
                break

    for idx, truck_route in enumerate(parent_2):
        for sol in truck_route:
            if sol.n_order < r_cross:
                continue
            else:
                new_sol[idx].append(sol)
    return new_sol


#TODO: do zmiany na ruletke:
def selection_rank(population, scores):
    sel_lst = []
    
    for ix in range(len(population)):
        if len(sel_lst) == 0:
            sel_lst.append((population[ix],scores[ix]))

        if scores[ix] > sel_lst[-1][1]:
            if len(sel_lst) >= n_pop:
                sel_lst[-1] = (population[ix],scores[ix])
            elif len(sel_lst) < n_pop:
                sel_lst.append((population[ix],scores[ix]))
        sel_lst.sort(reverse = 1, key = lambda x: x[1])
    
    return sel_lst

def create_structures(rows_cols: int, low_adj_matrix, high_adj_matrix: float, n_of_orders: int):
    # graf:
    g = Graph(rows_cols, rows_cols)
    g.create_adj_matrix(low_adj_matrix, high_adj_matrix)
    # lista ciężarówek:
    trucks_list = [Truck(TruckType.SMALL) for _ in range(n_small_trucks)]
    for _ in range(n_large_trucks):
        trucks_list.append(Truck(TruckType.LARGE))
    # lista zleceń:
    orders_lst = [Order(g, 20) for _ in range(n_of_orders)]
    return g, trucks_list, orders_lst
    

def selection(population_scores: List[tuple[int, int]], population_size: int):
    population_scores.sort(key = lambda x: x[1])
    selected = population_scores[0:population_size]
    return selected

def selection_rank():
    pass

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

    




    
a = [(1,11),(2,22),(3,33),(5,55),(4,44),(6,66)] 
npop= 4
print(selection_prop(a, npop))
    
#TODO: do dodania rodzice do nastepnego pokolenia:
def algorithm(n_iteration: int , r_cross: float, r_mutation: float, truck_list: List[Truck], order_lst: List[Order], g: Graph):
    children = []
    population = generate_solution(truck_list, order_lst, n_large_trucks, n_small_trucks)
    print(population[0])
    best, best_eval = population[0], objective_function(population[0], g, truck_list, order_lst, uncomplete_sol=False)
    for _ in range(n_iteration):
        if len(population) < 3:
            break
        else:
            population_scores = [(osobnik_id, objective_function(osobnik, g, truck_list, order_lst)) for osobnik_id, osobnik in enumerate(population)]
            # tymczasowe rozwiązanie selekcji:
            selected = selection(population_scores, 500)
            # print(selected)
            best, best_eval = population[selected[0][0]], objective_function(population[selected[0][0]], g, truck_list, order_lst)
            # print(best_eval)
            for i in range(0, len(selected)-1, 2):
                # print(len(population))
                parent_1, parent_2 = population[selected[i][0]], population[selected[i+1][0]]
                child = crossing(parent_1, parent_2, r_cross)
                new_child = mutation(child, truck_list, r_mutation)
                children.append(new_child)
                children.append(choice([parent_1, parent_2]))
            new_population = children
            population_sort = (population, population_scores)
            # population_sort = population_sort.sort(key = lambda x: x[1])
            # population_sort = slice(len(population_sort)*parent_percent/100)
            slice_par = slice(3)
            print (population_sort[slice_par])


        
    return best, best_eval


