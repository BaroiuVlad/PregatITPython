if __name__ == '__main__':
    tasks = []

    while True:
        print("\n-- To-Do List --")
        print("1. Adauga sarcina")
        print("2. Vezi sarcinile")
        print("3. Sterge sarcina")
        print("4. Iesire")

        choice = input("Enter your choice: ")

        if choice == "1":
            introduced_task = input("Introdu descrierea sarcinii: ")
            tasks.append(introduced_task)

        elif choice == "2":
            if not tasks:
                print("Lista de sarcini este goala")
            else:
                print("\n Lista de sarcini ")
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")

        elif choice == "3":
            if not tasks:
                print("Lista de sarcini este goala")
            else:
                print("\n Lista de sarcini ")
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")

                try:
                    task_number = int(input("Introdu numarul sarcinii pe care vrei sa o stergi "))
                    if 1 <= task_number <= len(tasks):
                        deleted_task = tasks.pop(task_number - 1)
                        print(f" Sarcina '{deleted_task}' a fost stearsa cu succes")
                    else:
                        print("Nu exista sarcina la indexul introdus")
                except ValueError:
                    print("Introdu un numar valid!!!")

        elif choice == "4":
            print("Aplicatia se inchide")
            break
        else:
            print("Optiune invalida! Numarul ales trebuie sa fie intre 1-4")


