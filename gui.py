import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path
import main
import sys
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import src.algorithm


class Redirect():

    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see("end")


cwd = Path().cwd()
json_path = cwd / 'data' / 'variables.json'
try:
    with open(json_path) as f:
        init_variables = json.load(f)
except FileNotFoundError:
    init_variables = None

# Create the main window
ds_window = tk.Tk()
ds_window.title("Data Structures - Variable Setter")

mainFrame = tk.Frame(ds_window)
mainFrame.grid()

# var_names = ["SIMULATION_TIME", "speed_l", "capacity_l", "speed_s", "capacity_s", "n_small_trucks",
#              "n_large_trucks", "n_pop", "n_iteration", "penalty_factor", "r_mutation", "parent_percent"]

integer_str_vars = ["SIMULATION_TIME", "capacity_l", "capacity_s",
                "n_small_trucks", "n_large_trucks", "rows_cols", "low_adj_matrix", "high_adj_matrix", "n_of_orders"]
structures_vars = ["SIMULATION_TIME", "rows_cols", "low_adj_matrix", "high_adj_matrix", "n_of_orders", "n_small_trucks", 
                   "n_large_trucks", "speed_s", "capacity_s", "speed_l", "capacity_l"]

# save to json
def save_json():
    # Write the dictionary to a JSON file
    cwd = Path.cwd()
    var_path = cwd / 'data' / 'variables.json'
    with open(var_path, "w") as f:
        json.dump(variables, f)


#TODO: validate added variables like n_of_orders, and graph connected vars:
def validate_data_and_append(checked_value, structures_vars):
    # first validate and append for structures_vars list:
    if len(checked_value) == 0:
        return f'{structures_vars} should be filled'
    if structures_vars in integer_str_vars:
        try:
            int_value = int(checked_value)
            if int_value - float(checked_value) != 0:
                return f'{structures_vars} should be integer'
            if structures_vars == 'n_small_trucks':
                if int_value < 0:
                    return f'{structures_vars} should be non-negative'
            elif structures_vars == 'n_large_trucks':
                if int_value < 0:
                    return f'{structures_vars} should be non-negative'
                # TODO: zmien to, żeby zawsze brało 'n_large_trucks' a nie było zależne od kolejności
                if int_value + variables['structures_data']['n_small_trucks'] == 0:
                    return f'There should be at least one truck'
            # elif var_name == 'r_cross':
            #     if int_value < 0:
            #         return f'{var_name} should be non-negative'
            else:
                if int_value <= 0:
                    return f'{structures_vars} should be positive'

        except ValueError:
            return f'{structures_vars} should be integer'

        else:
            variables["structures_data"][structures_vars] = int_value
            return 'Success'

    else:
        try:
            if ',' in checked_value:
                return "Please use '.' as a decimal separator, instead of ','"
            # raises ValueError when conversion is not possible
            float_value = float(checked_value)

            if structures_vars == 'r_mutation':
                if float_value > 1:
                    return 'r_mutation should be lower or equal to 1'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            elif structures_vars == 'parent_percent':
                if float_value > 100:
                    return 'parent_percent should be lower or equal to 100'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            else:
                if float_value <= 0:
                    return f'{structures_vars} should be positive'

        except ValueError:
            return f'{structures_vars} should be float'

        else:
            variables["structures_data"][structures_vars] = float_value
            return 'Success'
    

# Create a function to save the data_structures values from the entries:
def save_str_values():
        # Create a list to hold the variables
    global variables
    variables = {
                "structures_data": {},
                "algorithm_data": {},
            }
    try:
        for idx, entry in enumerate(entries):
            checked_value = entry.get()
            msg = validate_data_and_append(
                checked_value, structures_vars[idx])
            if msg != 'Success':
                raise ValueError
    except ValueError:
        messagebox.showerror('Value Error', msg)
    else:
        save_json()
    create_alg_window()


def create_struct():
    src.algorithm.create_structures(variables['structures_data']["rows_cols"], 
                                    variables['structures_data']["low_adj_matrix"], 
                                    variables['structures_data']["high_adj_matrix"], 
                                    variables['structures_data']["n_of_orders"])
    
    
def show_plot():
    plot_window = tk.Tk()
    plot_window.geometry("800x600")
    plot_window.title("Results and Plot")
    plot_path = cwd / 'data' / 'wykres_funkcji_celu.png'
    plot_image = Image.open(plot_path)
    
    width = plot_window.winfo_screenwidth()
    height = plot_window.winfo_screenheight()
    x = (width - plot_window.winfo_reqwidth()) // 2
    y = (height - plot_window.winfo_reqheight()) // 2
    plot_window.geometry(f"+{x}+{y}")
    
    fig, ax = plt.subplots()
    fig.set_size_inches(width/100, height/100, forward=True)
    
    # Add the plot to the axes
    ax.imshow(plot_image)
    ax.set_axis_off()

    # text1 = tk.Text(plot_window, width=200, height=10)
    # text1.grid(row=9,columnspan=5)

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def run_algorithm():
    # function used in "run algorithm" button
    # that saves the output of main()
    global output
    output = main.main()


def show_output():
    # function used in "show output" button
    # prints saved output of main() to another window
    output_window = tk.Tk()
    output_window.title("Final Result Window")
    width = output_window.winfo_screenwidth()
    height = output_window.winfo_screenheight()
    x = (width - output_window.winfo_reqwidth()) // 2
    y = (height - output_window.winfo_reqheight()) // 2
    output_window.geometry(f"+{x}+{y}")
    text = tk.Text(output_window)
    text.pack(fill=tk.BOTH, expand=1) # set the fill and expand options to make the widget resize with the window
    text.insert('end', output)



# Create the entries and add them to the window
entries = []
for i in range(len(structures_vars)):
    # Create a label for the entry
    label = tk.Label(text="{}".format(structures_vars[i]))
    label.grid(row=(i//5)*2, column=i % 5)

    # Create the entry
    entry = tk.Entry(ds_window, width=20)
    if init_variables is not None:
        entry.insert(tk.END, init_variables['structures_data'][structures_vars[i]])
    entry.grid(row=(i//5)*2+1, column=i % 5)
    entries.append(entry)


# Create a button to get the values from the entries:
save_values_button = tk.Button(ds_window, text="Save Values", command=save_str_values)
save_values_button.grid(row=10, column=0, columnspan=2)

create_struct_button = tk.Button(ds_window, text="Create struct", command=create_struct)
create_struct_button.grid(row=10, column=3, columnspan=2)

#TODO: button to display the data structures:

# -------------------------------------ALGORYTM WINDOW-------------------------------------
algorithm_vars = ["n_pop", "n_iterations", "penalty_factor", "r_mutation", "parent_percent"]
integer_alg_vars = ["n_pop", "n_iteration"]


# Create a function to save the values from the entries
def save_alg_values():
        # Create a list to hold the variables
    global variables
    try:
        for idx, entry in enumerate(entries_alg):
            checked_value = entry.get()
            msg = validate_data_and_append_alg(
                checked_value, algorithm_vars[idx])
            if msg != 'Success':
                raise ValueError
    except ValueError:
        messagebox.showerror('Value Error', msg)
    else:
        # print(variables)
        save_json()
    
def get_values_unc_sol_sele():
    value_uc_sol = uncomplete_sol.get()
    value_select = selection_type.get()
    variables["algorithm_data"]["uncomplete_sol"] = value_uc_sol
    variables["algorithm_data"]["selection_type"] = value_select
    
def validate_data_and_append_alg(checked_value, algorithm_vars):
    # first validate and append for structures_vars list:
    if len(checked_value) == 0:
        return f'{algorithm_vars} should be filled'
    if algorithm_vars in integer_str_vars:
        try:
            int_value = int(checked_value)
            if int_value - float(checked_value) != 0:
                return f'{algorithm_vars} should be integer'
            if algorithm_vars == 'n_small_trucks':
                if int_value < 0:
                    return f'{algorithm_vars} should be non-negative'
            elif algorithm_vars == 'n_large_trucks':
                if int_value < 0:
                    return f'{algorithm_vars} should be non-negative'
                # TODO: zmien to, żeby zawsze brało 'n_large_trucks' a nie było zależne od kolejności
                if int_value + variables['structures_data']['n_small_trucks'] == 0:
                    return f'There should be at least one truck'
            # elif var_name == 'r_cross':
            #     if int_value < 0:
            #         return f'{var_name} should be non-negative'
            else:
                if int_value <= 0:
                    return f'{algorithm_vars} should be positive'

        except ValueError:
            return f'{algorithm_vars} should be integer'

        else:
            print(variables)
            variables["algorithm_data"][algorithm_vars] = int_value
            return 'Success'

    else:
        try:
            if ',' in checked_value:
                return "Please use '.' as a decimal separator, instead of ','"
            # raises ValueError when conversion is not possible
            float_value = float(checked_value)

            if algorithm_vars == 'r_mutation':
                if float_value > 1:
                    return 'r_mutation should be lower or equal to 1'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            elif algorithm_vars == 'parent_percent':
                if float_value > 100:
                    return 'parent_percent should be lower or equal to 100'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            else:
                if float_value <= 0:
                    return f'{algorithm_vars} should be positive'

        except ValueError:
            return f'{algorithm_vars} should be float'

        else:
            variables["algorithm_data"][algorithm_vars] = float_value
            return 'Success'
        

def create_alg_window():
    alg_window = tk.Tk()
    alg_window.title("Algorithm - Set Variables & Results")
    # Create the entries and add them to the window
    global entries_alg
    entries_alg = []
    for i in range(len(algorithm_vars)):
        # Create a label for the entry
        label_alg = tk.Label(alg_window, text="{}".format(algorithm_vars[i]))
        label_alg.grid(row=(i//5)*2+1, column=i % 5)

        # Create the entry
        entry = tk.Entry(alg_window, width=20)
        if init_variables is not None:
            entry.insert(tk.END, init_variables['algorithm_data'][algorithm_vars[i]])
        entry.grid(row=(i//5)*2+2, column=i % 5)
        entries_alg.append(entry)
    
    save_alg_values_button = tk.Button(alg_window, text="Save algorithm param.", command=save_alg_values)
    save_alg_values_button.grid(row=10, column=0, sticky=tk.E + tk.W)
    # Create a button for running algorithm
    run_algorithm_button = tk.Button(alg_window, text="Run algorithm", command=run_algorithm)
    run_algorithm_button.grid(row=10, column=1, sticky=tk.E + tk.W)

    show_results_button = tk.Button(alg_window, text="Show Results", command=show_plot)
    show_results_button.grid(row=10, column=2, sticky=tk.E + tk.W)

    show_output_button = tk.Button(alg_window, text="Show output", command=show_output)
    show_output_button.grid(row=10, column=3, sticky=tk.E + tk.W)

    show_values_button = tk.Button(alg_window, text="Uncomplete sol, selection", command=get_values_unc_sol_sele)
    show_values_button.grid(row=10, column=4, sticky=tk.E + tk.W)
    
    global uncomplete_sol, selection_type
    uncomplete_sol = tk.BooleanVar()
    selection_type = tk.StringVar()
    # Checkbox and radiobox section
    if init_variables is not None:
        uncomplete_sol.set(init_variables['algorithm_data']['uncomplete_sol'])
    
    c1 = tk.Checkbutton(alg_window, text="Allow creating uncomplete solutions during crossing",
                            variable=uncomplete_sol, onvalue=True, offvalue=False)
    c1.grid(row=6, column=2)

    if init_variables is not None:
        selection_type.set(init_variables['algorithm_data']["selection_type"])
    else:
        selection_type.initialize("selection")
    r1 = tk.Radiobutton(alg_window, text="selection",
                        variable=selection_type, value="selection")
    r1.grid(row=7, column=1, columnspan=2)
    r2 = tk.Radiobutton(alg_window, text="selection_tour",
                        variable=selection_type, value="selection_tour")
    r2.grid(row=7, column=2, columnspan=2)
    r3 = tk.Radiobutton(alg_window, text="selection_prop",
                        variable=selection_type, value="selection_roulette")
    r3.grid(row=8, column=1, columnspan=2)
    r4 = tk.Radiobutton(alg_window, text="selection_rank",
                        variable=selection_type, value="selection_rank")
    r4.grid(row=8, column=2, columnspan=2)
    

# text = tk.Text(window, width=200, height=10)
# text.grid(row=9,columnspan=5)

# old_stdout = sys.stdout
# sys.stdout = Redirect(text)
ds_window.eval('tk::PlaceWindow . center')
# Run the main loop
ds_window.mainloop()

# sys.stdout = old_stdout
