from algorithm import selection_prop, selection_tour, selection

a = [(0, 1),(1,11),(2,22),(3,33),(5,55),(4,44),(6,66)] 
npop= 2

# print(selection(a, npop))
print(selection_tour(a, npop))
# print(selection_prop(a, npop))