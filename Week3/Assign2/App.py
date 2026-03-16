from Task_system import TaskManager
from Custom_exceptions import (
    InvalidInputError,
    TaskNotFoundError,
    InvalidStatusTransitionError,
    EmptyUndoStackError
)


def main():
    manager = TaskManager()

    while True:
        print("\n--- Sistem de Management al Task-urilor ---")
        print("1. Creeaza Task")
        print("2. Listeaza Task-uri")
        print("3. Vizualizeaza detalii Task")
        print("4. Actualizeaza Task")
        print("5. Schimba statusul unui Task")
        print("6. Undo (Anuleaza ultima actiune)")
        print("7. Iesire")

        option = input("Selecteaza o optiune (1-7): ")

        try:
            if option == '1':
                title = input("Titlu: ")
                owner = input("Responsabil (Owner): ")
                desc = input("Descriere: ")
                manager.create_task(title, owner, desc)
                print(">> Task creat si salvat cu succes!")

            elif option == '2':
                sort_by = input("Sorteaza dupa (id, owner, status, updated_at) [apasa Enter pentru id]: ").strip()
                if not sort_by:
                    sort_by = "id"

                tasks = manager.list_tasks(sort_by=sort_by)
                if not tasks:
                    print(">> Nu exista task-uri inregistrate.")
                else:
                    for t in tasks:
                        print(t)

            elif option == '3':
                task_id = int(input("Introdu ID-ul task-ului: "))
                task = manager.get_task_by_id(task_id)
                print(f"\n--- Detalii Task [{task._id}] ---")
                print(f"Titlu: {task._title}")
                print(f"Responsabil: {task._owner}")
                print(f"Status: {task._status}")
                print(f"Descriere: {task._description}")
                print(f"Creat la: {task._created_at}")
                print(f"Ultima actualizare: {task._updated_at}")

            elif option == '4':
                task_id = int(input("Introdu ID-ul task-ului pe care vrei sa il modifici: "))
                title = input("Titlu nou (apasa Enter pentru a sari): ")
                owner = input("Responsabil nou (apasa Enter pentru a sari): ")
                desc = input("Descriere noua (apasa Enter pentru a sari): ")

                manager.update_task(
                    task_id,
                    title if title else None,
                    owner if owner else None,
                    desc if desc else None
                )
                print(">> Task actualizat cu succes!")

            elif option == '5':
                task_id = int(input("Introdu ID-ul task-ului: "))
                new_status = input("Status nou (ex: IN_PROGRESS, BLOCKED, DONE): ")

                manager.change_status(task_id, new_status)
                print(">> Status actualizat cu succes!")

            elif option == '6':
                manager.undo_last_action()
                print(">> Ultima actiune a fost anulata cu succes (Undo)!")

            elif option == '7':
                print("Se inchide aplicatia. La revedere!")
                break

            else:
                print("Optiune invalida. Te rog sa alegi un numar intre 1 si 7.")


        except InvalidInputError as e:
            print(f"[Eroare de Validare] {e}")
        except TaskNotFoundError as e:
            print(f"[Eroare] {e}")
        except InvalidStatusTransitionError as e:
            print(f"[Eroare Workflow] {e}")
        except EmptyUndoStackError as e:
            print(f"[Info] {e}")

        except ValueError:
            print("[Eroare] Asigura-te ca introduci numere valide pentru ID-uri.")

        except Exception as e:
            print(f"[Eroare Neasteptata] A aparut o problema: {e}")


if __name__ == "__main__":
    main()