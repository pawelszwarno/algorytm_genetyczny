from main import main
from typing import List
from random import sample
import numpy as np


# moja (PSu) implementacja ruletki
def selection_roulette(population_scores: List[tuple[int, int]], population_size: int):
    scores = np.array([score for _, score in population_scores])
    total_score = scores.sum()
    scores = scores / total_score
    new_scores = 1/scores
    new_total_score = new_scores.sum()
    probabilities = new_scores / new_total_score
    indices = np.arange(len(population_scores))
    selected_indices = np.random.choice(indices, size=population_size, p=probabilities, replace=False)
    return [population_scores[i] for i in selected_indices]


def selection_tour(population_scores: List[tuple[int, int]], population_size: int):
    selected = []
    population = [item[0] for item in population_scores]
    while len(selected) < population_size:
        tour = sample(population, min(3, len(population)))
        tour_scores = [(index, score) for index, score in population_scores if index in tour]
        tour_scores.sort(key = lambda x: x[1], reverse = True)
        winner = tour_scores[0]
        selected.append(winner)
        population.remove(winner[0])
    return selected


population_scores = [(0, 100), (1, 90), (2,120), (3,160), (4, 100), (5, 90), (6,120), (7,160), (8, 100), (9, 90), (10,120), (11,160)] 
population_scores2 = [(0, 10), (1, 5), (2, 12), (3, 10), (4, 16), (5, 4), (6, 2), (8, 14), (9, 22), (10, 12), (11, 11)]
population_scores3 = [(0, 1), (1, 8), (2, 10), (3, 20)]

# selection_tour
# print(selection_tour(population_scores, 4))
# print(selection_tour(population_scores2, 4))

# selection_prop
print(selection_roulette(population_scores, 3))
print(selection_roulette(population_scores3, 2))





