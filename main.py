from algorithm import generate_solution
from classes import Order, Truck, TruckType, Graph
from variables import n_pop

def main():
    # stworzenie grafu:
    g = Graph(6, 6)
    g.create_adj_matrix(0, 10)
    print("Macierz sąsiedztwa: ")
    print(g, '\n')
     
    # stworzenie listy ciężarówek:
    n_small_trucks = 7
    n_large_trucks = 6
    trucks_list = [Truck(TruckType.SMALL) for _ in range(n_small_trucks)]
    for _ in range(n_large_trucks):
        trucks_list.append(Truck(TruckType.LARGE))
    print("Lista ciężarówek: (Index, typ)")
    print(trucks_list, '\n')
    
    # Stworzenie listy zleceń złożonej z instancji klasy Order z polami:
    # deadline - czyli czas w którym trzeba dostarczyć dostawę i * 1000 (wyrażany w minutach np.)
    orders_lst = [Order(g, 20) for i in range(20)]
    print("Lista zleceń: ")
    print(orders_lst, '\n')
    # lista zleceń, liczba dużych ciężarówek, liczba małych ciężarówek,
    # pojemność małych ciężarówek, pojemność dużych ciężarówek
    
    # wygenerowanie początkowego rozwiązania i przedstawienie postaci rozwiązania:
    
    for i in range(n_pop):
        print("Osobnik {}".format(i))
        sol = generate_solution(trucks_list, orders_lst, n_large_trucks, n_small_trucks)
        for truck in trucks_list:
            print('Trasa ciężarówki nr {0}: {1}'.format(truck.index, sol[truck.index]))
        

if __name__ == "__main__":
    main()