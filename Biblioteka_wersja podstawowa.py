books = [
    {"title": "Wiedźmin", "author": "Andrzej Sapkowski", "copies": 3},
    {"title": "Lśnienie", "author": "Stephen King", "copies": 2},
    {"title": "Hobbit", "author": "J.R.R. Tolkien", "copies": 5},
    {"title": "Rok 1984", "author": "George Orwell", "copies": 1},
    {"title": "Zbrodnia i kara", "author": "Fiodor Dostojewski", "copies": 4}
]

users = [
    {"login": "jan", "password": "123", "role": "czytelnik"},
    {"login": "ania", "password": "abc", "role": "czytelnik"},
    {"login": "piotr", "password": "qwe", "role": "czytelnik"}
]
rentals = {
    "jan": [],
    "ania": [],
    "piotr": []
}

def login():
    """Obsługuje proces logowania użytkownika z limitem 3 prób."""
    attempts = 0
    while attempts < 3:
        login_input = input("Podaj login: ")
        password_input = input("Podaj hasło: ")
        
        for user in users:
            if user["login"] == login_input and user["password"] == password_input:
                print(f"Zalogowano pomyślnie. Witaj {login_input}!")
                return login_input
        
        attempts += 1
        print(f"Błędny login lub hasło. Pozostało prób: {3 - attempts}")
        
    print("Przekroczono limit prób logowania. Zamykanie programu.")
    return None

def display_catalog():
    """Wyświetla wszystkie dostępne książki i ich liczbę."""
    print("\n--- KATALOG KSIĄŻEK ---")
    for book in books:
        print(f"Tytuł: '{book['title']}', Autor: {book['author']} | Dostępne sztuki: {book['copies']}")
    print("-----------------------\n")

def borrow_book(current_user_login):
    """Pozwala wypożyczyć książkę zalogowanemu użytkownikowi."""
    book_title = input("Podaj tytuł książki, którą chcesz wypożyczyć: ")

    for book in books:

        if book["title"].lower() == book_title.lower():
            if book["copies"] > 0:
                book["copies"] -= 1 # Zmniejszamy liczbę dostępnych sztuk
                rentals[current_user_login].append(book["title"]) # Dodajemy do wypożyczeń użytkownika
                print(f"Pomyślnie wypożyczono książkę: '{book['title']}'.")
                return
            else:
                print(f"Niestety, brak wolnych egzemplarzy książki '{book['title']}'.")
                return
            
    print("Nie znaleziono książki o takim tytule w naszym katalogu.")

def display_user_rentals(current_user_login):
    """Wyświetla książki wypożyczone przez użytkownika."""
    user_books = rentals[current_user_login]
    print("\n--- TWOJE WYPOŻYCZENIA ---")
    if not user_books:
        print("Obecnie nie masz wypożyczonych żadnych książek.")
    else:
        for title in user_books:
            print(f"- {title}")
    print("--------------------------\n")

def menu(current_user_login):
    """Wyświetla główne menu i obsługuje wybór akcji."""
    while True:
        print("\n=== MENU GŁÓWNE ===")
        print("1. Przeglądaj katalog")
        print("2. Wypożycz książkę")
        print("3. Moje wypożyczenia")
        print("4. Wyloguj")
        
        choice = input("Wybierz opcję (1-4): ")
        
        if choice == '1':
            display_catalog()
        elif choice == '2':
            borrow_book(current_user_login)
        elif choice == '3':
            display_user_rentals(current_user_login)
        elif choice == '4':
            print(f"Wylogowano użytkownika '{current_user_login}'. Do zobaczenia!")
            break
        else:
            print("Niepoprawny wybór. Wybierz numer od 1 do 4.")

def main():
    """Główna funkcja spinająca cały program."""
    print("Witaj w systemie bibliotecznym!")
    current_user = login()
    
    if current_user:
        menu(current_user)

if __name__ == "__main__":
    main()