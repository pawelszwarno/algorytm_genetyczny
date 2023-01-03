def main():

    import json
    from pathlib import Path
    import src.algorithm as algorithm
    from src.classes import Order, Truck, TruckType, Graph
    from src.algorithm import visualise
    from io import StringIO
    import sys

    cwd = Path().cwd()
    json_path = cwd / 'data' / 'variables.json'
    with open(json_path) as f:
        variables = json.load(f)

    g, trucks_list, orders_lst = algorithm.create_structures(
        rows_cols=6, low_adj_matrix=0, high_adj_matrix=10, n_of_orders=40)

    # Save the current stdout
    original_stdout = sys.stdout

    # Create a buffer to hold the output
    output_buffer = StringIO()

    # Redirect the output to the buffer
    sys.stdout = output_buffer

    selection = getattr(algorithm, variables['selection_type'])
    best, best_eval, best_eval_list, iteration_eval_list = algorithm.algorithm(
        variables['n_iteration'], variables['r_cross'], variables['r_mutation'], trucks_list, orders_lst, g, selection, variables['uncomplete_sol'])
    print("Najlepsze rozwiązanie:")
    for line in best:
        print(line)
    print("O wartości funkcji celu: {}".format(int(best_eval)))
    Order.reset_id()
    Truck.reset_id()
    algorithm.visualise(best_eval_list, iteration_eval_list)

    # Reset the stdout to the original
    sys.stdout = original_stdout

    # Get the output as a string
    output_string = output_buffer.getvalue()

    # Return the output string
    return output_string


if __name__ == "__main__":
    main()
