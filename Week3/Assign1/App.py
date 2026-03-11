from Task_system import TaskManager


def main():
    manager = TaskManager()

    while True:
        print("\n--- Sistem de Management al Task-urilor ---")
        print("1. Creeaza Task")
        print("2. Listeaza Task-uri")
        print("3. Vizualizeaza detalii Task")
        print("4. Actualizeaza Task")
        print("5. Schimba statusul unui Task")
        print("6. Iesire")

        option = input("Selecteaza o optiune (1-6): ")

        try:
            if option == '1':
                title = input("Titlu: ")
                owner = input("Responsabil (Owner): ")
                desc = input("Descriere: ")
                manager.create_task(title, owner, desc)
                print("Task creat si salvat cu succes!")

            elif option == '2':
                tasks = manager.list_tasks()
                if not tasks:
                    print("Nu exista task-uri inregistrate.")
                else:
                    for t in tasks:
                        print(t)

            elif option == '3':
                task_id = int(input("Introdu ID-ul task-ului: "))
                task = manager.get_task_by_id(task_id)
                if task:
                    print(f"\n--- Detalii Task [{task._id}] ---")
                    print(f"Titlu: {task._title}")
                    print(f"Responsabil: {task._owner}")
                    print(f"Status: {task._status}")
                    print(f"Descriere: {task._description}")
                    print(f"Creat la: {task._created_at}")
                    print(f"Ultima actualizare: {task._updated_at}")
                else:
                    print("Task-ul nu a fost gasit.")

            elif option == '4':
                task_id = int(input("Introdu ID-ul task-ului pe care vrei sa il modifici: "))
                title = input("Titlu nou (apasa Enter pentru a sari): ")
                owner = input("Responsabil nou (apasa Enter pentru a sari): ")
                desc = input("Descriere noua (apasa Enter pentru a sari): ")

                success = manager.update_task(
                    task_id,
                    title if title else None,
                    owner if owner else None,
                    desc if desc else None
                )

                if success:
                    print("Task actualizat cu succes!")
                else:
                    print("Task-ul nu a fost gasit.")

            elif option == '5':
                task_id = int(input("Introdu ID-ul task-ului: "))
                new_status = input("Status nou (ex: IN_PROGRESS, BLOCKED, DONE): ")

                success, mesaj = manager.change_status(task_id, new_status)
                print(mesaj)

            elif option == '6':
                print("Se inchide aplicatia. La revedere!")
                break

            else:
                print("Optiune invalida. Te rog sa alegi un numar intre 1 si 6.")

        except ValueError:
            print("Eroare de introducere date! Asigura-te ca introduci numere pentru ID-uri.")
        except Exception as e:
            print(f"A aparut o eroare neasteptata: {e}")


if __name__ == "__main__":
    main()