from multiprocessing import Process, Semaphore, Lock
from random import randrange
from time import sleep, perf_counter
from datetime import datetime


def is_locked(lock):
    locked = lock.acquire(block=False)
    if locked == False:
        return True
    else:
        lock.release()
        return False


class Philosopher(Process):
    def __init__(self, id, dinner):
        Process.__init__(self)
        self.id = id
        self.seat = -1
        self.curr_reading = -1
        self.read = []
        self.dinner = dinner

    def choose_book(self):
        b = randrange(self.dinner.how_many_books)
        while b in self.read or is_locked(self.dinner.books[b]):
            b = randrange(self.dinner.how_many_books)
        self.dinner.books[b].acquire()
        print("{} bierze książkę {}.   [{}]".format(self.id, b, datetime.now().strftime("%H:%M:%S.%f")))
        self.curr_reading = b
        self.read.append(b)
        sleep(0.2)

    def return_book(self):
        print(
            "{} odkłada książkę {}. na półkę. Przeczytał już: {}   [{}]".format(
                self.id, self.curr_reading, self.read, datetime.now().strftime("%H:%M:%S.%f")
            )
        )
        self.dinner.books[self.curr_reading].release()
        sleep(0.2)

    def take_seat(self):
        if self.dinner.waiter:
            self.dinner.waiter.acquire()
            print("Kelner wpuścił {}.   [{}]".format(self.id, datetime.now().strftime("%H:%M:%S.%f")))
        s = randrange(self.dinner.how_many_seats)
        while is_locked(self.dinner.seats[s]):
            s = randrange(self.dinner.how_many_seats)
        self.dinner.seats[s].acquire()
        self.seat = s
        print("{} usiadł na miejscu {}.   [{}]".format(self.id, s, datetime.now().strftime("%H:%M:%S.%f")))
        sleep(0.25)

    def pick_forks_up(self):
        s = self.seat
        s2 = (s + 1) % self.dinner.how_many_seats
        forks = (False, False)
        while forks != (True, True):
            if not is_locked(self.dinner.forks[s]):
                self.dinner.forks[s].acquire()
                forks = (True, forks[1])
                sleep(0.1)
                print("{} wziął lewy widelec ({}).   [{}]".format(self.id, s, datetime.now().strftime("%H:%M:%S.%f")))
            if not is_locked(self.dinner.forks[s2]):
                self.dinner.forks[s2].acquire()
                forks = (forks[0], True)
                sleep(0.1)
                print(
                    "{} wziął prawy widelec ({}).   [{}]".format(self.id, s2, datetime.now().strftime("%H:%M:%S.%f"))
                )

    def eat(self):
        print("{} ma oba widelce i zaczyna jeść.   [{}]".format(self.id, datetime.now().strftime("%H:%M:%S.%f")))
        sleep(1)
        print("{} skończył jeść.   [{}]".format(self.id, datetime.now().strftime("%H:%M:%S.%f")))

    def put_forks_down(self):
        s = self.seat
        s2 = (s + 1) % self.dinner.how_many_seats
        self.dinner.forks[s].release()
        self.dinner.forks[s2].release()
        print("{} odłożył lewy widelec (<{}).   [{}]".format(self.id, s, datetime.now().strftime("%H:%M:%S.%f")))
        print("{} odłożył prawy widelec (<{}).   [{}]".format(self.id, s2, datetime.now().strftime("%H:%M:%S.%f")))
        sleep(0.1)

    def leave_table(self):
        self.dinner.seats[self.seat].release()
        print("{} wstaje i odchodzi od stołu.   [{}]".format(self.id, datetime.now().strftime("%H:%M:%S.%f")))
        if self.dinner.waiter:
            self.dinner.waiter.release()

    def run(self):
        while len(self.read) != self.dinner.how_many_books:
            self.choose_book()
            self.take_seat()
            self.pick_forks_up()
            self.eat()
            self.put_forks_down()
            self.leave_table()
            self.return_book()
        print(
            "{} przeczytał wszystkie książki i wychodzi.   [{}]".format(
                self.id, datetime.now().strftime("%H:%M:%S.%f")
            )
        )


class ProcessDinner:
    def __init__(self, guests_list: list, how_many_books: int):
        self.guests = guests_list
        self.how_many_seats = len(guests_list)
        self.seats = [Lock() for guest in guests_list]
        self.forks = [Lock() for guest in guests_list]
        self.waiter = Semaphore(len(guests_list) - 1)
        self.how_many_books = how_many_books
        self.books = [Lock() for i in range(how_many_books)]

    def start(self):
        print(
            "\n{}   ZACZYNAMY UCZTĘ   -   implementacja wieloprocesowa\n".format(
                datetime.now().strftime("%H:%M:%S.%f")
            )
        )
        t1 = perf_counter()
        philosophers = []
        for guest in self.guests:
            philosophers.append(Philosopher(guest, self))
        for philosopher in philosophers:
            philosopher.start()
        for philosopher in philosophers:
            philosopher.join()
        t2 = perf_counter()
        print("\n{}   UCZTA ZAKOŃCZONA. WSZYSCY GOŚCIE WYSZLI\n".format(datetime.now().strftime("%H:%M:%S.%f")))
        print("Czas trwania uczty:", round(t2 - t1, 6), "sekund   -   implementacja wieloprocesowa\n")
