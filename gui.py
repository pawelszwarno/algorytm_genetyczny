import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

cwd = Path().cwd()
json_path = cwd / 'data' / 'variables.json'
try:
    with open(json_path) as f:
        init_variables = json.load(f)
except FileNotFoundError:
    init_variables = None

# Create the main window
window = tk.Tk()
window.title("Variable Setter")

var_names = ["SIMULATION_TIME", "speed_l", "capacity_l", "speed_s", "capacity_s", "n_small_trucks", "n_large_trucks", "n_pop", "n_iteration", "penalty_factor", "r_cross", "r_mutation", "parent_percent", "uncomplete_sol"]
integer_vars = ["SIMULATION_TIME", "capacity_l", "capacity_s", "n_small_trucks", "n_large_trucks", "n_pop", "n_iteration", "r_cross"]
# Create a function to run the other functions that use the variables
def run_functions():
    # Write the dictionary to a JSON file
    cwd = Path.cwd()
    var_path = cwd / 'data' / 'variables.json'
    with open(var_path, "w") as f:
        json.dump(variables, f)

# Create a list to hold the variables
variables = {}

def validate_data_and_append(checked_value, var_name):
    if len(checked_value) == 0:
        return f'{var_name} should be filled'
    if var_name in integer_vars:
        try:
            int_value = int(checked_value)
            if int_value - float(checked_value) != 0:
                return f'{var_name} should be integer'
            if var_name == 'n_small_trucks':
                if int_value < 0:
                    return f'{var_name} should be non-negative'
            elif var_name == 'n_large_trucks':
                if int_value < 0:
                    return f'{var_name} should be non-negative'
                # TODO: zmien to, żeby zawsze brało 'n_large_trucks' a nie było zależne od kolejności
                if int_value + variables['n_small_trucks'] == 0:
                    return f'There should be at least one truck'
            elif var_name == 'r_cross':
                if int_value < 0:
                    return f'{var_name} should be non-negative'
            else:
                if int_value <= 0:
                    return f'{var_name} should be positive'
            
        except ValueError:
            return f'{var_name} should be integer'
        
        else:
            variables[var_name] = int_value
            return 'Success'
     
    else:
        try:
            float_value = float(checked_value) # raises ValueError when conversion is not possible
            
            if var_name == 'r_mutation':
                if float_value > 1:
                    return f'r_mutation should be lower or equal to 1'
                if float_value < 0:
                    return f'r_mutation should be higher or equal to 0'
            elif var_name == 'parent_percent':
                if float_value > 100:
                    return f'parent_percent should be lower or equal to 100'
                if float_value < 0:
                    return f'r_mutation should be higher or equal to 0'                
            else: 
                if float_value <= 0:
                    return f'{var_name} should be positive'
        
        except ValueError:
            return f'{var_name} should be float'
        
        else:
            variables[var_name] = float_value
            return 'Success'
            
    

# Create a function to get the values from the entries
def get_values():
    global variables
    variables = {}
    try:
        for idx, entry in enumerate(entries):
            checked_value = entry.get()
            msg = validate_data_and_append(checked_value, var_name=var_names[idx])
            if msg != 'Success':
                raise ValueError
        variables['uncomplete_sol'] = uncomplete_sol.get()
        variables['selection_type'] = selection_type.get()
    except ValueError:
        messagebox.showerror('Value Error', msg)
    else:
        run_functions()

# Create the entries and add them to the window
entries = []
for i in range(len(var_names)-1):
    # Create a label for the entry
    label = tk.Label(text="{}".format(var_names[i]))
    label.pack()

    # Create the entry
    entry = tk.Entry(window, width=20)
    if init_variables is not None:
        entry.insert(tk.END, init_variables[var_names[i]])
    entry.pack()
    entries.append(entry)

# Checkbox and radiobox section
uncomplete_sol = tk.BooleanVar()
if init_variables is not None:
    uncomplete_sol.initialize(init_variables['uncomplete_sol'])
c1 = tk.Checkbutton(window, text="Allow creating uncomplete solutions during crossing", variable=uncomplete_sol, onvalue=True, offvalue=False)
c1.pack()

selection_type = tk.StringVar()
if init_variables is not None:
    selection_type.initialize(init_variables["selection_type"])
else:
    selection_type.initialize("selection")
r1 = tk.Radiobutton(window, text="selection",  variable = selection_type, value = "selection")
r1.pack()
r2 = tk.Radiobutton(window, text="selection_tour", variable = selection_type, value = "selection_tour")
r2.pack()
r3 = tk.Radiobutton(window, text="selection_prop",  variable = selection_type, value = "selection_prop")
r3.pack()



# Create a button to get the values from the entries
get_values_button = tk.Button(text="Save Values", command=get_values)
get_values_button.pack()

# Run the main loop
window.mainloop()
