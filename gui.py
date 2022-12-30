import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

# Create the main window
window = tk.Tk()
window.title("Variable Setter")

var_names = ["SIMULATION_TIME", "speed_l", "capacity_l", "speed_s", "capacity_s", "n_small_trucks", "n_large_trucks", "n_pop", "n_iteration", "penalty_factor", "r_cross", "r_mutation", "parent_percent"]
integer_vars = ["SIMULATION_TIME", "capacity_l", "capacity_s", "n_small_trucks", "n_large_trucks", "n_pop", "n_iteration", "r_cross"]
# Create a function to run the other functions that use the variables
def run_functions():
    # Save the variables to a dictionary
    data = {"{}".format(var_names[i]): variables[i] for i in range(len(variables))}
    # Write the dictionary to a JSON file
    cwd = Path.cwd()
    var_path = cwd / 'data' / 'variables.json'
    with open(var_path, "w") as f:
        json.dump(data, f)

# Create a list to hold the variables
variables = []

def validate_data(checked_value, var_name):
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
                if int_value + var_names['n_small_trucks'] == 0:
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
            variables.append(int_value)
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
            variables.append(float_value)
            return 'Success'
            
    

# Create a function to get the values from the entries
def get_values():
    global variables
    variables = []
    try:
        for idx, entry in enumerate(entries):
            checked_value = entry.get()
            msg = validate_data(checked_value, var_name=var_names[idx])
            if msg != 'Success':
                raise ValueError
    except ValueError:
        messagebox.showerror('Value Error', msg)
    else:
        run_functions()

# Create the entries and add them to the window
entries = []
for i in range(len(var_names)):
    # Create a label for the entry
    label = tk.Label(text="{}".format(var_names[i]))
    label.pack()

    # Create the entry
    entry = tk.Entry(window, width=20)
    entry.pack()
    entries.append(entry)

# Create a button to get the values from the entries
get_values_button = tk.Button(text="Save Values", command=get_values)
get_values_button.pack()

# Run the main loop
window.mainloop()
