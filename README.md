## BADANIA OPERACYJNE 2:
Implementacja **algorytmu genetycznego** rozwiązującego zagadnienie transportowe.

## TODO:

### ALGORYTM:
- losowy r_cross, zamiast parametru

- Trzeba dodać opcję zachowania tych samych struktur danych (grafu i zleceń), aby móc przetestować wiele konfiguracji algorytmu i sprawdzić, która najlepsza dla tych samych danych. Osobne pierwsze okno gui (do tworzenia struktur)

- krzyżowanie - dodać drugie dziecko:
populacja = rodzice*parent_percent + dopchać dziećmi tyle że nie są brane po prostu najlpesze tylko według selekcji



### GUI:
- przycisk do samego create_structures i jakaś wizualizacja macierzy, i zeby można było 

- Idealnie byłoby mieć first window do zapisania parametrów, przycisk save values, przycisk run algorithm, który odpala wszystko ale nie pokazuje nic poza tym, potem show results i to jest text output z maina i w dodatku wykres.

- poprawić layout, oddzielić to od struktur danych i algorytmu, żeby były osobno


## UWAGI:
Napisałem selekcje turniejową i ruletke od nowa, teraz już działają ale chyba rankingowa jest optymalniejsza (nwm trzeba przetestować dla tych samych struktur danych),
na pewno jak wybieramy selekcje turniejową albo ruletke to trzeba zmniejszyć r_mut, bo sama selekcja wprowadza większą losowość.




### Skład grupy:
Paweł Szwarnowski
Mateusz Sztefko
Piotr Suchy