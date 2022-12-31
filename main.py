def main():

    import json
    from pathlib import Path
    import src.algorithm as algorithm
    from src.classes import Order, Truck, TruckType, Graph
    from src.algorithm import visualise
    
    cwd = Path().cwd()
    json_path = cwd / 'data' / 'variables.json'
    with open(json_path) as f:
        variables = json.load(f)
    
    g, trucks_list, orders_lst = algorithm.create_structures(rows_cols=6, low_adj_matrix=0, high_adj_matrix=10, n_of_orders=40)
    
    selection = getattr(algorithm, variables['selection_type'])
    best, best_eval, best_eval_list, iteration_eval_list = algorithm.algorithm(variables['n_iteration'], variables['r_cross'], variables['r_mutation'], trucks_list, orders_lst, g, selection, variables['uncomplete_sol'])
    print("Najlepsze rozwiązanie:")
    for line in best:
        print(line)
    print("O wartości funkcji celu: {}".format(int(best_eval)))
    Order.reset_id()
    Truck.reset_id()
    algorithm.visualise(best_eval_list, iteration_eval_list)
    return best, best_eval
        
    
if __name__ == "__main__":
    main()