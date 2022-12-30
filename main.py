import src.algorithm as algorithm
from src.classes import Order, Truck, TruckType, Graph


def main():
    # DO TESTOWANIA IN PROGRESS:
    # wygenerowanie początkowego rozwiązania i przedstawienie postaci rozwiązania:
    # sol = None
    # old_sol = None
    # for i in range(n_pop):
    #     print("Osobnik {}".format(i))
    #     old_sol = sol
    #     sol = generate_solution(trucks_list, orders_lst, n_large_trucks, n_small_trucks)
    #     for truck in trucks_list:
    #         print('Trasa ciężarówki nr {0}: {1}'.format(truck.index, sol[truck.index]))

    # print("Crossing:")
    # sol_po_crossingu = crossing(old_sol, sol, 10)
    # for truck in trucks_list:
    #     print('Trasa ciężarówki nr {0}: {1}'.format(truck.index, sol_po_crossingu[truck.index]))

    # print("Test mutacji: ")
    # sol_po_mutacji = mutation(sol_po_crossingu, trucks_list)
    # for truck in trucks_list:
    #     print('Trasa ciężarówki nr {0}: {1}'.format(truck.index, sol_po_mutacji[truck.index]))
    import json
    from pathlib import Path

    cwd = Path().cwd()
    json_path = cwd / 'data' / 'variables.json'
    with open(json_path) as f:
        variables = json.load(f)
    
    g, trucks_list, orders_lst = algorithm.create_structures(rows_cols=6, low_adj_matrix=0, high_adj_matrix=10, n_of_orders=40)
    # print("Macierz sąsiedztwa: \n {}".format(g))
    
    selection = getattr(algorithm, variables['selection_type'])
    best, best_eval = algorithm.algorithm(variables['n_iteration'], variables['r_cross'], variables['r_mutation'], trucks_list, orders_lst, g, selection, variables['uncomplete_sol'])
    print("Najlepsze rozwiązanie: \n {}".format(best))
    print("O wartości funkcji celu: {}".format(int(best_eval)))
        
    
if __name__ == "__main__":
    main()