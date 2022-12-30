import json
from gui import var_names

# Read the JSON file:
with open("variables.json", "r") as f:
    var_json = json.load(f)

# Retrieve the variables
SIMULATION_TIME = var_json["SIMULATION_TIME"]
speed_l = var_json["speed_l"]
capacity_l = var_json["capacity_l"]
speed_s = var_json["speed_s"]
capacity_s = var_json["capacity_s"]
n_small_trucks = var_json["n_small_trucks"]
n_large_trucks = var_json["n_large_trucks"]
n_pop = var_json["n_pop"]
n_iteration = var_json["n_iteration"]
penalty_factor = var_json["penalty_factor"]
r_cross = var_json["r_cross"]
r_mutation = var_json["r_mutation"]
parent_percent = var_json["parent_percent"]

# SIMULATION_TIME = 720  # 30 dni - 30*24 = 720h
# speed_l = 0.5
# capacity_l = 5

# speed_s = 0.3
# capacity_s = 3

# n_small_trucks = 3
# n_large_trucks = 3
# n_pop = 100

# n_iteration = 100
# penalty_factor = 100

# r_cross = 3
# r_mutation = 0.6

# parent_percent = 50 #procent rodziców przekazywany do następnej populacji 0-100%