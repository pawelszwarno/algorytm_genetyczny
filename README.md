## BADANIA OPERACYJNE 2:
Implementacja **algorytmu genetycznego** rozwiązującego zagadnienie transportowe.

## BŁĘDY:
ogólnie nie zapisuje się do variables.json uncomplete_sol i selection_type (linijka 247 około) (tak jakby .get() nie działał coś tam jest źle przypisane, idk męczyłem się z tym i nic nie znalazłem, za każdym razem bierze te pierwotne z inicjalizacji)

Poza tym pewnie jeszcze parę błędów bo nie wszystko byłem w stanie sprawdzić. Do zrobienia głównie z krzyżowaniem i żeby to dobrze działało powyżej. I ogarnięcie gui do normalnych standardów. Pare przycisków do usunięcia, bo były używane do sprawdzania czegoś (np. value uncomplete_sol i selection_type)
## TODO:

### ALGORYTM:
- losowy r_cross, zamiast parametru **#zrobione**

- Trzeba dodać opcję zachowania tych samych struktur danych (grafu i zleceń), aby móc przetestować wiele konfiguracji algorytmu i sprawdzić, która najlepsza dla tych samych danych. Osobne pierwsze okno gui (do tworzenia struktur) **#zrobione**, ale nie sprawdziłem, bo reszta do zrobienia jeszcze

- krzyżowanie - dodać drugie dziecko:
populacja = rodzice*parent_percent + dopchać dziećmi tyle że nie są brane po prostu najlpesze tylko według selekcji



### GUI:
- jakaś wizualizacja macierzy ewentualnie

- poprawić layout


## UWAGI:
do wklejenia jako variables.json na początek jakby były jakieś problemy
{
    "structures_data":
        {
            "SIMULATION_TIME": 720, "rows_cols": 6, "low_adj_matrix": 1, "high_adj_matrix": 10, "n_of_orders": 40, "n_small_trucks": 5, "n_large_trucks": 5, "speed_s": 2.0, "capacity_s": 5, "speed_l": 1.0, "capacity_l": 10
        },
        "algorithm_data":
        {
            "n_pop": 50, "n_iterations": 100, "penalty_factor": 100, "r_mutation": 0.5, "parent_percent": 0.5, "selection_type": "selection_rank", "uncomplete_sol": false
        }
}


### Skład grupy:
Paweł Szwarnowski
Mateusz Sztefko
Piotr Suchy