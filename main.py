from algorithm import generate_solution, crossing, mutation, algorithm, create_structures, selection, selection_tour
from classes import Order, Truck, TruckType, Graph, SelectionType
from variables import n_pop, n_large_trucks, n_small_trucks, n_iteration, r_cross, r_mutation


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
    
    g, trucks_list, orders_lst = create_structures(6, 0, 10, 20)
    # print("Macierz sąsiedztwa: \n {}".format(g))
    
    best, best_eval = algorithm(n_iteration, r_cross, r_mutation, trucks_list, orders_lst, g, selection, uncomplete_sol=False)
    print("Najlepsze rozwiązanie: \n {}".format(best))
    print("O wartości funkcji celu: {}".format(int(best_eval)))
        
    
if __name__ == "__main__":
    main()