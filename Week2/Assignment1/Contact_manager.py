contacts: list[dict] = []


def is_valid_phone(phone: str) -> bool:

    return len(phone) == 10 and phone.isdigit()


def is_valid_email(email: str) -> bool:

    return "@" in email and "." in email


def display_contact_details(contact: dict) -> None:

    print(f"\n--- Contact: {contact.get('name')} ---")
    for key, value in contact.items():
        print(f"{key.capitalize()}: {value}")


def add_contact(name: str, phone: str, **kwargs: str) -> None:

    # Validare nume
    if not name.strip():
        print("Eroare: Numele nu poate fi gol!")
        return

    # Validare telefon
    if not is_valid_phone(phone):
        print(f"Eroare: Numarul '{phone}' este invalid! Trebuie sa aiba 10 cifre.")
        return

    # Verificare duplicat (dupa telefon)
    for c in contacts:
        if c['phone'] == phone:
            print(f"Eroare: Numarul {phone} exista deja in lista!")
            return

    # Validare email daca exista in kwargs
    if 'email' in kwargs and not is_valid_email(kwargs['email']):
        print("Eroare: Formatul email-ului este invalid!")
        return

    # Creare dictionar contact
    new_contact = {'name': name, 'phone': phone}
    new_contact.update(kwargs)  # Adaugam campurile optionale din **kwargs

    contacts.append(new_contact)
    print(f"Contactul '{name}' a fost adaugat cu succes!")


def list_all_contacts(sort_key: str = 'name', reverse: bool = False) -> None:

    if not contacts:
        print("\nLista de contacte este goala.")
        return


    sorted_contacts = sorted(contacts, key=lambda c: str(c.get(sort_key, "")).lower(), reverse=reverse)

    print(f"\n--- Lista Contacte (Sortat dupa {sort_key}) ---")
    for contact in sorted_contacts:
        display_contact_details(contact)


def search_contacts(*args: str, **kwargs: str) -> None:
    results = []
    for contact in contacts:
        match = False


        for term in args:
            if contact['name'].lower().startswith(term.lower()) or contact['phone'].startswith(term):
                match = True


        for key, value in kwargs.items():
            if str(contact.get(key, "")).lower() == str(value).lower():
                match = True

        if match:
            results.append(contact)

    if results:
        print(f"\nS-au gasit {len(results)} rezultate:")
        for res in results:
            display_contact_details(res)
    else:
        print("\nNiciun contact gasit.")