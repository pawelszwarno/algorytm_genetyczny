def main(g, trucks_list, orders_lst):

    import json
    from pathlib import Path
    import src.algorithm as algorithm
    from src.classes import Order, Truck
    from io import StringIO
    import sys
    
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
    best, best_eval, best_eval_list, iteration_eval_list = algorithm.algorithm(variables, trucks_list, orders_lst, g, selection)
    print("Najlepsze rozwiązanie:")
    for line in best:
        print(line)
    print("O wartości funkcji celu: {}".format(int(best_eval)))
    algorithm.visualise(best_eval_list, iteration_eval_list)

    # Reset the stdout to the original
    sys.stdout = original_stdout

    # Get the output as a string
    output_string = output_buffer.getvalue()

    # Return the output string
    return output_string


if __name__ == "__main__":
    main()
