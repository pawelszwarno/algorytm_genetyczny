def main(g, trucks_list, orders_lst, n_of_runs, plot_title="wykres_funkcji_celu.png"):

    import json
    from pathlib import Path
    import src.algorithm as algorithm
    from src.classes import Order, Truck
    from io import StringIO
    import sys
    import matplotlib.pyplot as plt
    from time import time
    
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

    plt.figure()
    start = time()
    for _ in range(n_of_runs):
        selection = getattr(algorithm, variables["algorithm_data"]['selection_type'])
        best, best_eval, best_eval_list, iteration_eval_list = algorithm.algorithm(variables, trucks_list, orders_lst, g, selection)
        # print("Najlepsze rozwiązanie:")
        # for line in best:
        #     print(line)
        # print("O wartości funkcji celu: {}".format(int(best_eval)))

        plt.subplot(211)
        plt.plot(best_eval_list, label='Najlepsza wartość funkcji celu')
        plt.subplot(212)
        plt.plot(iteration_eval_list, label='Wartość funkcji celu w danej iteracji')
    end = time()
    print(f"Średni czas wykonania: {(end-start)/n_of_runs}")
    plt.subplot(211)
    plt.title('Najlepsza wartość funkcji celu')
    plt.xlabel('Nr iteracji')
    plt.subplot(212)
    plt.title('Wartość funkcji celu w danej iteracji')
    plt.ylabel('Wartość funkcji celu')
    plt.tight_layout()
    plt.savefig(f'data/{plot_title}', dpi=100)
    print(plot_title)

    # Reset the stdout to the original
    sys.stdout = original_stdout

    # Get the output as a string
    output_string = output_buffer.getvalue()

    # Return the output string
    return output_string


if __name__ == "__main__":
    main()
