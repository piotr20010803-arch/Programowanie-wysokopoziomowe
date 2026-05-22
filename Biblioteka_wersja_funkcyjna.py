class Book:
    def __init__(self, title, author, copies):
        self._title = title
        self._author = author
        self._total_copies = copies  # ile bylo na poczatku, potrzebne do statystyk
        self._available_copies = copies

    def get_title(self): return self._title
    def get_author(self): return self._author
    def get_available(self): return self._available_copies
    def get_total(self): return self._total_copies

    def borrow(self):
        if self._available_copies > 0:
            self._available_copies -= 1
            return True
        return False

    def __str__(self):
        return f"Tytuł: '{self._title}', Autor: {self._author} | Dostępne sztuki: {self._available_copies}"


class User:
    def __init__(self, login, password, role):
        self._login = login
        self._password = password
        self._role = role

    def get_login(self): return self._login
    def get_password(self): return self._password


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")
        self._rentals = []
        self._extension_requests = []
        self._reservations = []  # nowa lista na rezerwacje

    def get_rentals(self): return self._rentals
    def get_extension_requests(self): return self._extension_requests
    def get_reservations(self): return self._reservations
    def add_rental(self, title): self._rentals.append(title)
    def add_reservation(self, title): self._reservations.append(title)
    def remove_extension_request(self, title): self._extension_requests.remove(title)

    def request_extension(self, title):
        if title in self._rentals:
            self._extension_requests.append(title)
            return True
        return False


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "bibliotekarz")


class Library:
    def __init__(self):
        self._books = [
            Book("Wiedźmin", "Andrzej Sapkowski", 3),
            Book("Lśnienie", "Stephen King", 2),
            Book("Hobbit", "J.R.R. Tolkien", 5),
            Book("Rok 1984", "George Orwell", 1),
            Book("Zbrodnia i kara", "Fiodor Dostojewski", 4)
        ]
        self._users = [
            Reader("jan", "123"),
            Reader("ania", "abc"),
            Reader("piotr", "qwe"),
            Librarian("admin", "admin123")
        ]

    # funkcja wyzszego rzedu - przyjmuje predykat i zwraca przefiltrowane ksiazki
    def filter_catalog(self, predicate):
        return list(filter(predicate, self._books))

    # tez wyzszego rzedu - key_fn to funkcja ktora mowi po czym sortowac
    def sort_catalog(self, key_fn, reverse=False):
        return sorted(self._books, key=key_fn, reverse=reverse)

    def _print_books(self, books, label="KATALOG KSIĄŻEK"):
        print(f"\n--- {label} ---")
        if not books:
            print("Brak wyników.")
        else:
            # map ze str zeby wyswietlic kazda ksiazke bez petli for
            print("\n".join(map(str, books)))
        print("-" * (len(label) + 8) + "\n")

    def login(self):
        attempts = 0
        while attempts < 3:
            login_input = input("Podaj login: ")
            password_input = input("Podaj hasło: ")
            # filter zamiast petli for zeby znalezc usera
            matched = list(filter(
                lambda u: u.get_login() == login_input and u.get_password() == password_input,
                self._users
            ))
            if matched:
                print(f"Zalogowano pomyślnie. Witaj {login_input}!")
                return matched[0]
            attempts += 1
            print(f"Błędny login lub hasło. Pozostało prób: {3 - attempts}")
        print("Przekroczono limit prób logowania. Zamykanie programu.")
        return None

    def search_and_display(self):
        phrase = input("Podaj frazę (tytuł lub autor, Enter = pomiń): ").strip()
        only_available = input("Tylko dostępne? (t/n): ").lower() == "t"

        # dwie lambdy - jedna sprawdza fraze, druga dostepnosc
        phrase_filter = (lambda b: phrase.lower() in b.get_title().lower()
                                   or phrase.lower() in b.get_author().lower()) \
                        if phrase else (lambda b: True)
        avail_filter = (lambda b: b.get_available() > 0) if only_available else (lambda b: True)

        # laczę oba filtry w jedna lambde i przekazuje do filter_catalog
        books = self.filter_catalog(lambda b: phrase_filter(b) and avail_filter(b))
        self._print_books(books, "WYNIKI WYSZUKIWANIA")

    def display_sorted(self):
        print("\nSortuj według:")
        print("1. Tytuł")
        print("2. Autor")
        print("3. Dostępne sztuki")
        choice = input("Wybierz (1-3): ")

        # slownik z lambdami jako kluczami sortowania - wybieramy odpowiednia
        key_map = {
            "1": lambda b: b.get_title(),
            "2": lambda b: b.get_author(),
            "3": lambda b: b.get_available()
        }
        if choice not in key_map:
            print("Niepoprawny wybór.")
            return
        books = self.sort_catalog(key_map[choice])
        self._print_books(books, "POSORTOWANY KATALOG")

    def display_catalog(self):
        self._print_books(self._books)

    def borrow_book(self, reader):
        book_title = input("Podaj tytuł książki, którą chcesz wypożyczyć: ")
        # list comprehension zamiast petli do szukania ksiazki
        matched = [b for b in self._books if b.get_title().lower() == book_title.lower()]
        if not matched:
            print("Nie znaleziono książki o takim tytule w naszym katalogu.")
            return
        book = matched[0]
        if book.borrow():
            reader.add_rental(book.get_title())
            print(f"Pomyślnie wypożyczono książkę: '{book.get_title()}'.")
        else:
            decision = input(f"Brak wolnych egzemplarzy '{book.get_title()}'. Zarezerwować? (t/n): ")
            if decision.lower() == "t":
                if book.get_title() not in reader.get_reservations():
                    reader.add_reservation(book.get_title())
                    print(f"Zarezerwowano '{book.get_title()}'. Powiadomimy Cię, gdy będzie dostępna.")
                else:
                    print("Masz już rezerwację na tę książkę.")

    def display_user_rentals(self, reader):
        print("\n--- TWOJE WYPOŻYCZENIA ---")
        if not reader.get_rentals():
            print("Obecnie nie masz wypożyczonych żadnych książek.")
        else:
            print("\n".join(map(lambda t: f"  - {t}", reader.get_rentals())))
        if reader.get_reservations():
            print("\n--- TWOJE REZERWACJE ---")
            print("\n".join(map(lambda t: f"  * {t}", reader.get_reservations())))
        print("--------------------------\n")

    def request_extension(self, reader):
        book_title = input("Podaj tytuł książki, o której przedłużenie prosisz: ")
        if reader.request_extension(book_title):
            print(f"Prośba o przedłużenie książki '{book_title}' została wysłana.")
        else:
            print("Nie masz wypożyczonej takiej książki.")

    def display_all_rentals(self):
        print("\n--- WSZYSTKIE WYPOŻYCZENIA ---")
        # dict comprehension - loguję czytelnikow którzy cos maja wypozyczone
        rentals_by_reader = {u.get_login(): u.get_rentals()
                             for u in self._users
                             if isinstance(u, Reader) and u.get_rentals()}
        if not rentals_by_reader:
            print("Nikt nie ma aktualnie wypożyczonych książek.")
        else:
            for login, titles in rentals_by_reader.items():
                print(f"Użytkownik: {login}")
                print("\n".join(map(lambda t: f"  - {t}", titles)))
        print("------------------------------\n")

    def handle_extension_requests(self):
        print("\n--- PROŚBY O PRZEDŁUŻENIE ---")
        # plaska lista wszystkich rezerwacji z comprehension zagniezdzonego
        all_reservations = [title
                            for u in self._users if isinstance(u, Reader)
                            for title in u.get_reservations()]
        any_found = False
        for user in self._users:
            if isinstance(user, Reader) and user.get_extension_requests():
                any_found = True
                for title in list(user.get_extension_requests()):
                    # pokazujemy ile osob czeka na ta ksiazke jesli ktos czeka
                    reservation_count = all_reservations.count(title)
                    res_info = f" [UWAGA: {reservation_count} rezerwacja/e na ten tytuł]" \
                               if reservation_count > 0 else ""
                    print(f"Użytkownik '{user.get_login()}' prosi o przedłużenie: '{title}'{res_info}")
                    decision = input("Zaakceptować? (t/n): ")
                    user.remove_extension_request(title)
                    print("Prośba zaakceptowana." if decision.lower() == "t" else "Prośba odrzucona.")
        if not any_found:
            print("Brak próśb o przedłużenie.")
        print("-----------------------------\n")

    def display_statistics(self):
        print("\n--- STATYSTYKI BIBLIOTEKI ---")
        # list comprehension - tylko czytelnicy
        readers = [u for u in self._users if isinstance(u, Reader)]

        # sortuję po liczbie wypożyczeń malejąco i biorę pierwszego - to najpopularniejsza
        most_popular = sorted(self._books,
                              key=lambda b: b.get_total() - b.get_available(),
                              reverse=True)[0]
        borrowed_count = most_popular.get_total() - most_popular.get_available()
        print(f"Najpopularniejsza książka: '{most_popular.get_title()}' ({borrowed_count} wypożyczeń)")

        # map zwraca liczby wypozyczen dla kazdego czytelnika, sum je sumuje
        total_rentals = sum(map(lambda r: len(r.get_rentals()), readers))
        print(f"Aktywne wypożyczenia łącznie: {total_rentals}")

        # sorted z lambda po liczbie wypozyczen
        sorted_readers = sorted(readers, key=lambda r: len(r.get_rentals()), reverse=True)
        print("\nCzytelnicy wg aktywności:")
        print("\n".join(map(lambda r: f"  {r.get_login()}: {len(r.get_rentals())} tytułów", sorted_readers)))
        print("-----------------------------\n")

    def reader_menu(self, reader):
        while True:
            print("\n=== MENU GŁÓWNE ===")
            print("1. Przeglądaj katalog")
            print("2. Wyszukaj / filtruj książki")
            print("3. Posortowany katalog")
            print("4. Wypożycz książkę")
            print("5. Moje wypożyczenia i rezerwacje")
            print("6. Poproś o przedłużenie")
            print("7. Wyloguj")
            choice = input("Wybierz opcję (1-7): ")
            if choice == "1": self.display_catalog()
            elif choice == "2": self.search_and_display()
            elif choice == "3": self.display_sorted()
            elif choice == "4": self.borrow_book(reader)
            elif choice == "5": self.display_user_rentals(reader)
            elif choice == "6": self.request_extension(reader)
            elif choice == "7":
                print(f"Wylogowano użytkownika '{reader.get_login()}'. Do zobaczenia!")
                break
            else: print("Niepoprawny wybór.")

    def librarian_menu(self, librarian):
        while True:
            print("\n=== MENU BIBLIOTEKARZA ===")
            print("1. Przeglądaj katalog")
            print("2. Wyszukaj / filtruj książki")
            print("3. Posortowany katalog")
            print("4. Lista wszystkich wypożyczeń")
            print("5. Obsłuż prośby o przedłużenie")
            print("6. Statystyki")
            print("7. Wyloguj")
            choice = input("Wybierz opcję (1-7): ")
            if choice == "1": self.display_catalog()
            elif choice == "2": self.search_and_display()
            elif choice == "3": self.display_sorted()
            elif choice == "4": self.display_all_rentals()
            elif choice == "5": self.handle_extension_requests()
            elif choice == "6": self.display_statistics()
            elif choice == "7":
                print(f"Wylogowano bibliotekarza '{librarian.get_login()}'. Do zobaczenia!")
                break
            else: print("Niepoprawny wybór.")

    def run(self):
        print("Witaj w systemie bibliotecznym!")
        user = self.login()
        if user:
            if isinstance(user, Librarian):
                self.librarian_menu(user)
            else:
                self.reader_menu(user)


if __name__ == "__main__":
    library = Library()
    library.run()
