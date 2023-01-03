## BADANIA OPERACYJNE 2:
Implementacja **algorytmu genetycznego** rozwiązującego zagadnienie transportowe.

## TODO:

### ALGORYTM:
- Trzeba dodać opcję zachowania tych samych struktur danych (grafu i zleceń), aby móc przetestować wiele konfiguracji algorytmu i sprawdzić, która najlepsza dla tych samych danych.
- sprawdzić jak z algorytmem z parent_percent - bo mamy w algorithm() linijke z 'children.append(choice([parent_1, parent_2]))' gdzie dodawany jest parent nie patrzac jaki jest parent_percent.
- może dodać do rozw. jakis znacznik refillowania? może niepotrzebne


### GUI:
- Aktualna wersja output z maina pokazywany w nowym oknie dopiero po kliknięciu "Show output" - ale można wrócić do wersji wczesniejszej z text outputem.
- Idealnie byłoby mieć first window do zapisania parametrów, przycisk save values, przycisk run algorithm, który odpala wszystko ale nie pokazuje nic poza tym, potem show results i to jest text output z maina i w dodatku wykres.

## UWAGI:
Napisałem selekcje turniejową i ruletke od nowa, teraz już działają ale chyba rankingowa jest optymalniejsza (nwm trzeba przetestować dla tych samych struktur danych),
na pewno jak wybieramy selekcje turniejową albo ruletke to trzeba zmniejszyć r_mut, bo sama selekcja wprowadza większą losowość.


### Skład grupy:
Paweł Szwarnowski
Mateusz Sztefko
Piotr Suchy