if __name__ == '__main__':
    birthdate = input("birthdate DD/MM/YYYY: ")
    name = input("name: ")
    country = input("country: ")

    is_valid = True

    if len(birthdate) != 10:
        print("Eroare: Data trebuie sa aiba exact 10 caractere (ex: 01/02/2000).")
        is_valid = False
    else:
        parts = [birthdate[0:2], birthdate[3:5], birthdate[6:10]]

        is_numeric = [p.isdigit() for p in parts]

        if False in is_numeric:
            print("Datele trebuie sa fie formate doar din numere.")
            is_valid = False
        else:
            date_parts = [int(x) for x in parts]
            day, month, year = date_parts

            if month > 12 or month < 1:
                print("Luna nu este valida (1-12).")
                is_valid = False
            elif day > 31 or day < 1:
                print("Ziua nu este valida (1-31).")
                is_valid = False
            elif year < 1900 or year > 2026:
                print("Anul nu este valid.")
                is_valid = False

    if is_valid:
        current_year = 2026
        age = current_year - year

        driving_age = 18
        voting_age = 18

        if country.lower() == "usa" or country.lower() == "sua":
            driving_age = 16

        if age >= voting_age:
            print(f"Felicitari, {name}, ai varsta necesara pentru a vota in {country}!")

        if age >= driving_age:
            print(f"Felicitari, {name}, ai varsta necesara pentru a conduce in {country}!")