import msvcrt
from multiprocessingDinner import ProcessDinner
from multithreadingDinner import ThreadDinner


if __name__ == "__main__":
    print(
        "\nRozwiązanie klasycznego problemu ucztujących filozofów z drobną zmianą - filozofowie podczas jedzenia czytają, a uczta kończy się, gdy wszyscy filozofowie przeczytają wszystkie książki. Nad porządkiem przy stole czuwa kelner, który dopuszcza do stołu maksymalnie czterech gości jednocześnie. Do wyboru są dwie implementacje: wielowątkowa i wieloprocesowa.\n"
    )
    guests = ["Sokrates", "Platon", "Arystoteles", "Kant", "Nietzsche"]
    while True:
        print(
            "Wybierz:\n1, aby uruchomić implementację wielowątkową\n2, aby uruchomić implementację wieloprocesową\nEsc, aby wyjść"
        )
        option = msvcrt.getch()
        print(option.decode(), "\n")
        if option == chr(27).encode():
            break
        elif option == chr(49).encode() or option == chr(50).encode():
            while True:
                try:
                    how_many_books = int(
                        input("Wprowadź liczbę książek, które mają przeczytać filozofowie i naciśnij Enter: ")
                    )
                    dinner = (
                        ThreadDinner(guests, how_many_books)
                        if option == chr(49).encode()
                        else ProcessDinner(guests, how_many_books)
                    )
                    dinner.start()
                    break
                except:
                    print("Nieprawidłowa wartość! Liczba książek musi być liczbą całkowitą!\n")
        else:
            print("Wprowadzono nieprawidłową wartość. Wybierz jedną z dostępnych opcji\n")
