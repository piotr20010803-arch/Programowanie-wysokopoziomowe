# klasa dla ksiazki, trzyma tytul autora i ile egzemplarzy jest dostepnych
class Book:
    def __init__(self, title, author, copies):
        self._title = title
        self._author = author
        self._available_copies = copies  # ile mozna jeszcze wypozyczyc

    def get_title(self): return self._title
    def get_available(self): return self._available_copies

    def borrow(self):
        # zmniejszamy licznik jak ktos bierze ksiazke, jak 0 to false
        if self._available_copies > 0:
            self._available_copies -= 1
            return True
        return False

    def __str__(self):
        # to sie wyswietla gdy robimy print(book)
        return f"Tytuł: '{self._title}', Autor: {self._author} | Dostępne sztuki: {self._available_copies}"


# klasa bazowa dla uzytkownika, reader i librarian po niej dziedzicza
class User:
    def __init__(self, login, password, role):
        self._login = login      # pola z _ sa "prywatne" (hermetyzacja)
        self._password = password
        self._role = role

    def get_login(self): return self._login
    def get_password(self): return self._password


# czytelnik - moze wypozyczyc ksiazke i prosic o przedluzenie
class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")  # wywoluje __init__ z User
        self._rentals = []            # lista wypozyczonych ksiazek
        self._extension_requests = [] # lista prosb o przedluzenie

    def get_rentals(self): return self._rentals
    def get_extension_requests(self): return self._extension_requests
    def add_rental(self, title): self._rentals.append(title)
    def remove_extension_request(self, title): self._extension_requests.remove(title)

    def request_extension(self, title):
        # mozna prosic tylko o te ktore sie ma wypozyczone
        if title in self._rentals:
            self._extension_requests.append(title)
            return True
        return False


# bibliotekarz - dziedziczy po User ale nie ma listy wypozyczen
class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "bibliotekarz")


# glowna klasa - zarzadza wszystkim, tu jest cala logika
class Library:
    def __init__(self):
        # dane startowe jako obiekty klas (nie slowniki jak w wersji 1)
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

    def login(self):
        attempts = 0
        while attempts < 3:
            login_input = input("Podaj login: ")
            password_input = input("Podaj hasło: ")
            for user in self._users:
                if user.get_login() == login_input and user.get_password() == password_input:
                    print(f"Zalogowano pomyślnie. Witaj {login_input}!")
                    return user
            attempts += 1
            print(f"Błędny login lub hasło. Pozostało prób: {3 - attempts}")
        print("Przekroczono limit prób logowania. Zamykanie programu.")
        return None

    def display_catalog(self):
        print("\n--- KATALOG KSIĄŻEK ---")
        for book in self._books:
            print(book)  # tutaj dziala __str__ z klasy Book
        print("-----------------------\n")

    def borrow_book(self, reader):
        book_title = input("Podaj tytuł książki, którą chcesz wypożyczyć: ")
        for book in self._books:
            if book.get_title().lower() == book_title.lower():
                if book.borrow():  # borrow() zwraca True/False
                    reader.add_rental(book.get_title())
                    print(f"Pomyślnie wypożyczono książkę: '{book.get_title()}'.")
                else:
                    print(f"Niestety, brak wolnych egzemplarzy książki '{book.get_title()}'.")
                return
        print("Nie znaleziono książki o takim tytule w naszym katalogu.")

    def display_user_rentals(self, reader):
        books = reader.get_rentals()
        print("\n--- TWOJE WYPOŻYCZENIA ---")
        if not books:
            print("Obecnie nie masz wypożyczonych żadnych książek.")
        else:
            for title in books:
                print(f"- {title}")
        print("--------------------------\n")

    def request_extension(self, reader):
        book_title = input("Podaj tytuł książki, o której przedłużenie prosisz: ")
        if reader.request_extension(book_title):
            print(f"Prośba o przedłużenie książki '{book_title}' została wysłana.")
        else:
            print("Nie masz wypożyczonej takiej książki.")

    def display_all_rentals(self):
        # bibliotekarz widzi wypozyczenia wszystkich uzytkownikow
        print("\n--- WSZYSTKIE WYPOŻYCZENIA ---")
        any_found = False
        for user in self._users:
            if isinstance(user, Reader) and user.get_rentals():  # isinstance sprawdza typ obiektu
                any_found = True
                print(f"Użytkownik: {user.get_login()}")
                for title in user.get_rentals():
                    print(f"  - {title}")
        if not any_found:
            print("Nikt nie ma aktualnie wypożyczonych książek.")
        print("------------------------------\n")

    def handle_extension_requests(self):
        # bibliotekarz akceptuje albo odrzuca prosby o przedluzenie
        print("\n--- PROŚBY O PRZEDŁUŻENIE ---")
        any_found = False
        for user in self._users:
            if isinstance(user, Reader) and user.get_extension_requests():
                any_found = True
                for title in list(user.get_extension_requests()):  # list() zeby nie modyfikowac podczas petli
                    print(f"Użytkownik '{user.get_login()}' prosi o przedłużenie: '{title}'")
                    decision = input("Zaakceptować? (t/n): ")
                    user.remove_extension_request(title)
                    print("Prośba zaakceptowana." if decision.lower() == "t" else "Prośba odrzucona.")
        if not any_found:
            print("Brak próśb o przedłużenie.")
        print("-----------------------------\n")

    def reader_menu(self, reader):
        while True:
            print("\n=== MENU GŁÓWNE ===")
            print("1. Przeglądaj katalog")
            print("2. Wypożycz książkę")
            print("3. Moje wypożyczenia")
            print("4. Poproś o przedłużenie")
            print("5. Wyloguj")
            choice = input("Wybierz opcję (1-5): ")
            if choice == "1": self.display_catalog()
            elif choice == "2": self.borrow_book(reader)
            elif choice == "3": self.display_user_rentals(reader)
            elif choice == "4": self.request_extension(reader)
            elif choice == "5":
                print(f"Wylogowano użytkownika '{reader.get_login()}'. Do zobaczenia!")
                break
            else: print("Niepoprawny wybór. Wybierz numer od 1 do 5.")

    def librarian_menu(self, librarian):
        while True:
            print("\n=== MENU BIBLIOTEKARZA ===")
            print("1. Przeglądaj katalog")
            print("2. Lista wszystkich wypożyczeń")
            print("3. Obsłuż prośby o przedłużenie")
            print("4. Wyloguj")
            choice = input("Wybierz opcję (1-4): ")
            if choice == "1": self.display_catalog()
            elif choice == "2": self.display_all_rentals()
            elif choice == "3": self.handle_extension_requests()
            elif choice == "4":
                print(f"Wylogowano bibliotekarza '{librarian.get_login()}'. Do zobaczenia!")
                break
            else: print("Niepoprawny wybór. Wybierz numer od 1 do 4.")

    def run(self):
        print("Witaj w systemie bibliotecznym!")
        user = self.login()
        if user:
            # zaleznie od roli pokazujemy inne menu
            if isinstance(user, Librarian):
                self.librarian_menu(user)
            else:
                self.reader_menu(user)


if __name__ == "__main__":
    library = Library()
    library.run()
