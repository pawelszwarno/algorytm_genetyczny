## BADANIA OPERACYJNE 2:
Implementacja **algorytmu ewolucyjnego** rozwiązującego zagadnienie transportowe.

### TODO:
- Zfixować GUI do końca, drugie okno szczególnie, nwm czy dodawać przycisk do pokazania wyniku jako coś osobnego (output z maina przekierowywać dopiero gdy zostanie wciśnięty przycisk) czy zostawić tak jak jest. (Aktualna wersja output z maina pokazywany dopiero po kliknięciu "Show output")
- Idealnie byłoby mieć first window do zapisania parametrów, przycisk save values, przycisk run algorithm, który odpala wszystko ale nie pokazuje nic poza tym, potem show results i to jest text output z maina i w dodatku wykres.

- Trzeba dodać opcję zachowania tych samych struktur danych (grafu i zleceń), aby móc przetestować wiele konfiguracji algorytmu i sprawdzić, która najlepsza dla tych samych danych.

- selekcja ruletka i tournament nie działają podczas używania ich w gui (przynajmniej napewno gdy są niedozwolone rozwiązania) - są errory, do sfixowania:
**Przykład:**
  File "/Users/piotrsuchy/Desktop/Programming/anaconda/anaconda3/envs/piotrsuchy/lib/python3.9/tkinter/__init__.py", line 1892, in __call__
    return self.func(*args)
  File "/Users/piotrsuchy/Desktop/AGH/SEMESTR 5/Badania Operacyjne 2/AE-2/algorytm_genetyczny/main.py", line 17, in main
    best, best_eval, best_eval_list, iteration_eval_list = algorithm.algorithm(variables['n_iteration'], variables['r_cross'], variables['r_mutation'], trucks_list, orders_lst, g, selection, variables['uncomplete_sol'])
  File "/Users/piotrsuchy/Desktop/AGH/SEMESTR 5/Badania Operacyjne 2/AE-2/algorytm_genetyczny/src/algorithm.py", line 215, in algorithm
    population = generate_solution(truck_list, order_lst, variables['n_large_trucks'], variables['n_small_trucks'])
  File "/Users/piotrsuchy/Desktop/AGH/SEMESTR 5/Badania Operacyjne 2/AE-2/algorytm_genetyczny/src/algorithm.py", line 18, in generate_solution
    if solution[hired_truck.index]:
IndexError: list index out of range



### Skład grupy:
Paweł Szwarnowski
Mateusz Sztefko
Piotr Suchy