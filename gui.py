import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path
import main
import sys
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")


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
window = tk.Tk()
window.title("Variable Setter")

mainFrame = tk.Frame(window)
mainFrame.grid()

var_names = ["SIMULATION_TIME", "speed_l", "capacity_l", "speed_s", "capacity_s", "n_small_trucks",
             "n_large_trucks", "n_pop", "n_iteration", "penalty_factor", "r_cross", "r_mutation", "parent_percent"]
integer_vars = ["SIMULATION_TIME", "capacity_l", "capacity_s",
                "n_small_trucks", "n_large_trucks", "n_pop", "n_iteration", "r_cross"]


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
            if ',' in checked_value:
                return "Please use '.' as a decimal separator, instead of ','"
            # raises ValueError when conversion is not possible
            float_value = float(checked_value)

            if var_name == 'r_mutation':
                if float_value > 1:
                    return 'r_mutation should be lower or equal to 1'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            elif var_name == 'parent_percent':
                if float_value > 100:
                    return 'parent_percent should be lower or equal to 100'
                if float_value < 0:
                    return 'r_mutation should be higher or equal to 0'
            else:
                if float_value <= 0:
                    return f'{var_name} should be positive'

        except ValueError:
            return f'{var_name} should be float'

        else:
            variables[var_name] = float_value
            return 'Success'


# Create a function to save the values from the entries
def save_values():
    global variables
    variables = {}
    try:
        for idx, entry in enumerate(entries):
            checked_value = entry.get()
            msg = validate_data_and_append(
                checked_value, var_name=var_names[idx])
            if msg != 'Success':
                raise ValueError
        variables['uncomplete_sol'] = uncomplete_sol.get()
        variables['selection_type'] = selection_type.get()
    except ValueError:
        messagebox.showerror('Value Error', msg)
    else:
        run_functions()


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
for i in range(len(var_names)):
    # Create a label for the entry
    label = tk.Label(text="{}".format(var_names[i]))
    label.grid(row=(i//5)*2, column=i % 5)

    # Create the entry
    entry = tk.Entry(window, width=20)
    if init_variables is not None:
        entry.insert(tk.END, init_variables[var_names[i]])
    entry.grid(row=(i//5)*2+1, column=i % 5)
    entries.append(entry)

# Checkbox and radiobox section
uncomplete_sol = tk.BooleanVar()
if init_variables is not None:
    uncomplete_sol.initialize(init_variables['uncomplete_sol'])
c1 = tk.Checkbutton(window, text="Allow creating uncomplete solutions during crossing",
                    variable=uncomplete_sol, onvalue=True, offvalue=False)
c1.grid(row=6, column=2)

selection_type = tk.StringVar()
if init_variables is not None:
    selection_type.initialize(init_variables["selection_type"])
else:
    selection_type.initialize("selection")
r1 = tk.Radiobutton(window, text="selection",
                    variable=selection_type, value="selection")
r1.grid(row=8, column=1)
r2 = tk.Radiobutton(window, text="selection_tour",
                    variable=selection_type, value="selection_tour")
r2.grid(row=8, column=2)
r3 = tk.Radiobutton(window, text="selection_prop",
                    variable=selection_type, value="selection_prop")
r3.grid(row=8, column=3)


# Create a button to get the values from the entries
save_values_button = tk.Button(text="Save Values", command=save_values)
save_values_button.grid(row=10, column=0, columnspan=2)

# Create a button for running algorithm
run_algorithm_button = tk.Button(text="Run algorithm", command=run_algorithm)
run_algorithm_button.grid(row=10, column=1, columnspan=2)

show_results_button = tk.Button(text="Show Results", command=show_plot)
show_results_button.grid(row=10, column=2, columnspan=2)

show_output_button = tk.Button(window, text="Show output", command=show_output)
show_output_button.grid(row=10, column=3, columnspan=2)

# text = tk.Text(window, width=200, height=10)
# text.grid(row=9,columnspan=5)

# old_stdout = sys.stdout
# sys.stdout = Redirect(text)
window.eval('tk::PlaceWindow . center')
# Run the main loop
window.mainloop()

# sys.stdout = old_stdout
