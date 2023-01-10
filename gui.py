import tkinter as tk
from tkinter import messagebox, ttk, filedialog, Grid
import json
from jsonschema import validate
from pathlib import Path
import main
import sys
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import graph_visualisation


integer_str_vars = ["SIMULATION_TIME", "capacity_l", "capacity_s",
                "n_small_trucks", "n_large_trucks", "rows_cols", "low_adj_matrix", "high_adj_matrix", "n_of_orders", "max_pallets"]
structures_vars = ["SIMULATION_TIME", "rows_cols", "low_adj_matrix", "high_adj_matrix", "n_of_orders", "max_pallets",
                   "n_small_trucks", "n_large_trucks", "speed_s", "capacity_s", "speed_l", "capacity_l"]

proper_names_str = ["Simulation length (h)", "Number of rows and columns", "Min distance between stores", "Max distance between stores", "Number of orders",
                "Maximum number of pallets in one order", "Number of small trucks", "Number of large trucks", "Speed of small trucks [in units]", "Capacity of small trucks [in pallets]",
                "Speed of large trucks [in units]", "Capacity of large trucks [in pallets]"]



cwd = Path().cwd()
json_path = cwd / 'data' / 'variables.json'
json_schema_path = cwd / 'data' / 'json_schema.json'


with open(json_schema_path) as jf:
    schema = json.load(jf)
try:
    with open(json_path) as f:
        init_variables = json.load(f)
except FileNotFoundError:
    init_variables = None


def next_window():
    ds_window.destroy_window()
    create_alg_window()

# Create a function to save the data_structures values from the entries:
def generate_structures():
        # Create a list to hold the variables
    global variables
    if init_variables is None:
        variables = {
                    "structures_data": {},
                    "algorithm_data": {},
                }
    else:
        variables = init_variables.copy()
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
        g, trucks_list, orders_lst = create_struct()
        variables["Graph"] = g.matrix.tolist()
        variables["truck_list"] = []
        for truck in trucks_list:
            variables["truck_list"].append({"type": f"{truck.type}", "index": truck.index})

        variables["order_lst"] = []
        for order in orders_lst:
            variables["order_lst"].append({"n_pallets": order.n_pallets, "vertex": order.vertex,
                                                              "deadline": order.deadline, "index": order.index})

        save_json()
        if variables["structures_data"]["rows_cols"] <= 20:
            graph_visualisation.graph_visualise(g)
        


# Uploading values from JSON file
def upload_from_file():
    uploaded_file = filedialog.askopenfile(filetypes=[('JSON file', '*.json')])
    unvalidated_variables = json.load(uploaded_file)
    validate(instance=unvalidated_variables, schema=schema)
    global variables, init_variables
    variables = unvalidated_variables.copy()
    init_variables = variables.copy()
    save_json()
    ds_window.reopen()

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        global mainFrame
        mainFrame = tk.Frame(self)
        mainFrame.grid()

        self.title("Data Structures - Variable Setter")
        self.eval('tk::PlaceWindow . center')

        # Create the entries and add them to the window
        global entries
        entries = []
        for i in range(len(structures_vars)):
            # Create a label for the entry
            label = tk.Label(text="{}".format(proper_names_str[i]))
            label.grid(row=(i // 5) * 2, column=i % 5)

            # Create the entry
            entry = tk.Entry(self, width=20)
            if init_variables is not None:
                entry.insert(tk.END, init_variables['structures_data'][structures_vars[i]])
            entry.grid(row=(i // 5) * 2 + 1, column=i % 5)
            entries.append(entry)

        Grid.rowconfigure(self, 10, weight=1)
        for i in range(0, 6):
            Grid.columnconfigure(self, i, weight=1)

        # Create a button to get the values from the entries:
        save_values_button = tk.Button(self, text="Generate Structures", command=generate_structures)
        save_values_button.grid(row=10, column=0, columnspan=1)

        upload_from_file_button = tk.Button(self, text="Upload from file", command=upload_from_file)
        upload_from_file_button.grid(row=10, column=2, columnspan=1)

        next_window_button = tk.Button(self, text="Next Window", command=next_window)
        next_window_button.grid(row=10, column=4, columnspan=1)
        
        global text
        text = tk.Text(self, width=200, height=10)
        text.grid(row=11, columnspan=5, sticky="NSEW")

    def reopen(self):
        self.destroy()
        self.__init__()
        
    def destroy_window(self):
        self.destroy()




class Redirect:

    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see("end")



# Create the main window
ds_window = App()

# save to json
def save_json():
    # Write the dictionary to a JSON file
    cwd = Path.cwd()
    var_path = cwd / 'data' / 'variables.json'
    with open(var_path, "w") as f:
        json.dump(variables, f, indent=2)


def validate_data_and_append(checked_value, structure_var):
    # first validate and append for structures_vars list:
    if len(checked_value) == 0:
        return f'{structure_var} should be filled'
    if structure_var in integer_str_vars:
        try:
            int_value = int(checked_value)
            if int_value - float(checked_value) != 0:
                return f'{structure_var} should be integer'

            if structure_var == 'n_small_trucks':
                if int_value < 0:
                    return f'{structure_var} should be non-negative'
            elif structure_var == 'n_large_trucks':
                if int_value < 0:
                    return f'{structure_var} should be non-negative'
                if int_value + variables['structures_data']['n_small_trucks'] == 0:
                    return f'There should be at least one truck'
            elif structure_var == 'low_adj_matrix':
                if int_value < 0:
                    return f'{structure_var} should be non-negative'
            elif structure_var == 'high_adj_matrix':
                if int_value < 0:
                    return f'{structure_var} should be non-negative'
                if int_value < variables['structures_data']['low_adj_matrix']:
                    return f'{structure_var} should be greater than low_adj_matrix'
            else:
                if int_value <= 0:
                    return f'{structure_var} should be positive'

        except ValueError:
            return f'{structure_var} should be integer'

        else:
            variables["structures_data"][structure_var] = int_value
            return 'Success'

    else:
        try:
            if ',' in checked_value:
                return "Please use '.' as a decimal separator, instead of ','"
            # raises ValueError when conversion is not possible
            float_value = float(checked_value)
            if float_value <= 0:
                return f'{structure_var} should be positive'

        except ValueError:
            return f'{structure_var} should be float'

        else:
            variables["structures_data"][structure_var] = float_value
            return 'Success'
    



def create_struct():
    import src.algorithm
    rows_cols = variables["structures_data"]["rows_cols"]
    low_adj_matrix = variables["structures_data"]["low_adj_matrix"]
    high_adj_matrix = variables["structures_data"]["high_adj_matrix"]
    n_of_orders = variables["structures_data"]["n_of_orders"]
    max_pallets = variables["structures_data"]["max_pallets"]
    n_small_trucks = variables["structures_data"]['n_small_trucks']
    n_large_trucks = variables["structures_data"]['n_large_trucks']
    capacity_s = variables["structures_data"]['capacity_s']
    speed_s = variables["structures_data"]['speed_s']
    capacity_l = variables["structures_data"]['capacity_l']
    speed_l = variables["structures_data"]['speed_l']
    simulation_time = variables["structures_data"]['SIMULATION_TIME']

    global g, trucks_list, orders_lst
    g, trucks_list, orders_lst = src.algorithm.create_structures(rows_cols, low_adj_matrix, high_adj_matrix, n_of_orders, max_pallets, n_small_trucks, n_large_trucks, capacity_s, speed_s, capacity_l, speed_l, simulation_time)

    old_stdout = sys.stdout

    sys.stdout = Redirect(text)
    print("Macierz G: \n {}".format(g))
    print("Lista zleceń:")
    for zlecenie in orders_lst:
        print("{}".format(zlecenie))


    sys.stdout = old_stdout

    return g, trucks_list, orders_lst

    
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
    
    plt.figure()
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
    output = main.main(g, trucks_list, orders_lst)
    text_alg.insert('end', output)


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



# -------------------------------------ALGORYTM WINDOW-------------------------------------
algorithm_vars = ["n_pop", "n_iterations", "penalty_factor", "r_mutation", "parent_percent", "uncomplete_sol", "selection_type"]
integer_alg_vars = ["n_pop", "n_iterations"]
proper_names_alg = ["Number of members in the population", "Number of iterations", "Penalty factor [in units]", "Probability of mutation [0-1]", "Percentage of parents in the population"]

# Create a function to save the values from the entries
def save_alg_values():
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
        get_uncomplete_sol_selection_type()
        save_json()
    

def go_back():
    alg_window.destroy()
    global ds_window
    # Create the main window
    ds_window = App()


    
def get_uncomplete_sol_selection_type():
    c1_states = c1.state()
    r1_states = r1.state()
    r2_states = r2.state()
    r3_states = r3.state()
    r4_states = r4.state()
    if 'selected' in c1_states:
        variables['algorithm_data']['uncomplete_sol'] = True
    else:
        variables['algorithm_data']['uncomplete_sol'] = False
    if 'selected' in r1_states:
        variables['algorithm_data']['selection_type'] = "selection"
    elif 'selected' in r2_states:
        variables['algorithm_data']['selection_type'] = "selection_tour"
    elif 'selected' in r3_states:
        variables['algorithm_data']['selection_type'] = "selection_roulette"
    elif 'selected' in r4_states:
        variables['algorithm_data']['selection_type'] = "selection_rank"
    

def validate_data_and_append_alg(checked_value, algorithm_var):
    # first validate and append for structures_vars list:
    if len(checked_value) == 0:
        return f'{algorithm_var} should be filled'
    if algorithm_var in integer_alg_vars:
        try:
            int_value = int(checked_value)
            if int_value - float(checked_value) != 0:
                return f'{algorithm_var} should be integer'

            if int_value <= 0:
                return f'{algorithm_var} should be positive'

        except ValueError:
            return f'{algorithm_var} should be integer'

        else:
            variables["algorithm_data"][algorithm_var] = int_value
            return 'Success'

    else:
        try:
            if ',' in checked_value:
                return "Please use '.' as a decimal separator, instead of ','"
            # raises ValueError when conversion is not possible
            float_value = float(checked_value)

            if algorithm_var == 'r_mutation':
                if float_value > 1:
                    return 'r_mutation should be lower or equal to 1'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            elif algorithm_var == 'parent_percent':
                if float_value > 100:
                    return 'parent_percent should be lower or equal to 100'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            else:
                if float_value <= 0:
                    return f'{algorithm_var} should be positive'

        except ValueError:
            return f'{algorithm_var} should be float'

        else:
            variables["algorithm_data"][algorithm_var] = float_value
            return 'Success'
        

def create_alg_window():
    global alg_window
    alg_window = tk.Tk()
    alg_window.title("Algorithm - Set Variables & Results")
    alg_window.focus_force()
    
    Grid.rowconfigure(alg_window, 10, weight=1)
    for i in range(0, 6):
        Grid.columnconfigure(alg_window, i, weight=1)
    # Create the entries and add them to the window
    global entries_alg
    entries_alg = []
    for i in range(len(algorithm_vars)-2):
        # Create a label for the entry
        label_alg = tk.Label(alg_window, text="{}".format(proper_names_alg[i]))
        label_alg.grid(row=(i//5)*2+1, column=i % 5)

        # Create the entry
        entry = tk.Entry(alg_window, width=20)
        if init_variables is not None:
            entry.insert(tk.END, init_variables['algorithm_data'][algorithm_vars[i]])
        entry.grid(row=(i//5)*2+2, column=i % 5)
        entries_alg.append(entry)
    
    global uncomplete_sol_var, selection_type_var
    uncomplete_sol_var = tk.BooleanVar()
    selection_type_var = tk.StringVar()
    
    # Checkbox and radiobox section
    if init_variables is not None:
        uncomplete_sol_var.initialize(init_variables['algorithm_data']['uncomplete_sol'])
    else:
        uncomplete_sol_var.initialize(False)
    
    global c1, r1, r2, r3, r4
    c1 = ttk.Checkbutton(alg_window, text="Allow creating uncomplete solutions during crossing",
                            variable=uncomplete_sol_var, onvalue=True, offvalue=False)
    c1.grid(row=6, column=2)

    # if init_variables is not None:
    #     selection_type.set(init_variables['algorithm_data']["selection_type"])
    # else:
    #     selection_type.initialize("selection")


    r1 = ttk.Radiobutton(alg_window, text="Best Members Selection", variable=selection_type_var, value="selection")
    r1.grid(row=7, column=0, columnspan=2)
    r2 = ttk.Radiobutton(alg_window, text="Tournament Selection", variable=selection_type_var, value="selection_tour")
    r2.grid(row=7, column=1, columnspan=2)
    r3 = ttk.Radiobutton(alg_window, text="Roulette Wheel Selection", variable=selection_type_var, value="selection_roulette")
    r3.grid(row=7, column=2, columnspan=2)
    r4 = ttk.Radiobutton(alg_window, text="Ranking Selection", variable=selection_type_var, value="selection_rank")
    r4.grid(row=7, column=3, columnspan=2)
    
    save_alg_values_button = tk.Button(alg_window, text="Save Algorithm Parameters", command=save_alg_values)
    save_alg_values_button.grid(row=10, column=0, columnspan=2)
    # Create a button for running algorithm
    run_algorithm_button = tk.Button(alg_window, text="Run Algorithm", command=run_algorithm)
    run_algorithm_button.grid(row=10, column=1, columnspan=2)

    show_results_button = tk.Button(alg_window, text="Show Plot", command=show_plot)
    show_results_button.grid(row=10, column=2, columnspan=2)
    
    go_back_button = tk.Button(alg_window, text="Go Back to First Window", command=go_back)
    go_back_button.grid(row=10,column=3, columnspan=2)

    global text_alg
    text_alg = tk.Text(alg_window, width=200, height=10)
    text_alg.grid(row=11, columnspan=5, sticky="NSEW")

    old_stdout = sys.stdout

    sys.stdout = Redirect(text_alg)

    sys.stdout = old_stdout
    

# text = tk.Text(window, width=200, height=10)
# text.grid(row=9,columnspan=5)

# old_stdout = sys.stdout
# sys.stdout = Redirect(text)
ds_window.eval('tk::PlaceWindow . center')
# Run the main loop
ds_window.mainloop()

# sys.stdout = old_stdout
