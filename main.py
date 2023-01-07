def main():

    import json
    from pathlib import Path
    import src.algorithm as algorithm
    from src.classes import Order, Truck, TruckType, Graph
    from src.algorithm import visualise
    from io import StringIO
    import sys
    from create_struct import g, trucks_list, orders_lst
    
    cwd = Path().cwd()
    json_path = cwd / 'data' / 'variables.json'
    with open(json_path) as f:
        variables = json.load(f)

    # Save the current stdout
    original_stdout = sys.stdout

    # Create a buffer to hold the output
    output_buffer = StringIO()

    # Redirect the output to the buffer
    sys.stdout = output_buffer

    selection = getattr(algorithm, variables["algorithm_data"]['selection_type'])
    best, best_eval, best_eval_list, iteration_eval_list = algorithm.algorithm(
        variables["algorithm_data"]['n_iterations'], variables["algorithm_data"]['r_mutation'], trucks_list, orders_lst, g, selection, variables["algorithm_data"]['uncomplete_sol'])
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
