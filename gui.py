import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

# Create the main window
window = tk.Tk()
window.title("Variable Setter")

var_names = ["SIMULATION_TIME", "speed_l", "capacity_l", "speed_s", "capacity_s", "n_small_trucks", "n_large_trucks", "n_pop", "n_iteration", "penalty_factor", "r_cross", "r_mutation", "parent_percent"]
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

# Create a function to get the values from the entries
def get_values():
    global variables
    variables = []
    try:
        for entry in entries:
            variables.append(entry.get())
    except ValueError:
        messagebox.showerror('Value Error', 'Only integer values are accepted!')
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
