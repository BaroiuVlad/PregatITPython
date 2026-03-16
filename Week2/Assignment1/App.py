
from Contact_manager import add_contact, list_all_contacts, search_contacts


def main():

    while True:
        print("\n=== MENIU CONTACTE ===")
        print("1. Adauga Contact")
        print("2. Listeaza Contacte")
        print("3. Cauta Contact")
        print("4. Iesire")

        choice = input("Alegeti optiunea (1-4): ")

        if choice == '1':
            name = input("Nume: ")
            phone = input("Telefon (10 cifre): ")
            email = input("Email (optional - apasati Enter daca nu aveti): ")

            if email:
                add_contact(name, phone, email=email)
            else:
                add_contact(name, phone)

        elif choice == '2':
            key = input("Sortati dupa (name/phone): ") or "name"
            list_all_contacts(sort_key=key)

        elif choice == '3':
            query = input("Introduceti numele sau numarul pentru cautare: ")
            search_contacts(query)

        elif choice == '4':
            print("Aplicatia se inchide. La revedere!")
            break
        else:
            print("Optiune invalida! Incercati din nou.")


if __name__ == "__main__":
    main()