from main import main
from src.algorithm import selection_tour

#TODO: testowanie selekcji prop i tour:
population_scores = [(0, 100), (1, 90), (2,120), (3,160), (4, 100), (5, 90), (6,120), (7,160), (8, 100), (9, 90), (10,120), (11,160)] 
npop = 4

# output = main()

# selection_prop
# selection_tour
# print(output)
print(selection_tour(population_scores, 12))
# print(selection_prop(a, npop))



