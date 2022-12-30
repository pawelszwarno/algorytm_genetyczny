from algorithm import selection_prop, selection_tour, selection

population_scores = [(0, 100), (1, 90), (2,120), (3,160), (4, 100), (5, 90), (6,120), (7,160), (8, 100), (9, 90), (10,120), (11,160)] 
npop = 4

print(selection_tour(population_scores, npop))
# print(selection(population_scores, npop))
# print(selection_prop(a, npop))



