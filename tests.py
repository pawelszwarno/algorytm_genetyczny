from algorithm import selection_prop, selection_tour, selection

population_scores = [(0, 100),(1, 90),(2,120),(3,160),(5,80),(4,75),(6,95)] 
npop = 4

# print(selection_tour(a, npop))
print(selection(population_scores, npop))
# print(selection_prop(a, npop))


