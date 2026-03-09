from Data_store import EVENT_LOG, UNDO_STACK, add_event


def push_to_undo(event_id):
    UNDO_STACK.append(event_id)


def process_next_event():
    if not EVENT_LOG:
        print("\n Nu sunt evenimente de procesat.")
        return

    event = EVENT_LOG.pop(0)
    print(f"\nSe proceseaza: {event['name']} (ID: {event['id']})")


def undo_last_event():
    if not UNDO_STACK:
        print("\n Nu exista actiuni pentru Undo.")
        return

    last_id = UNDO_STACK.pop()

    for index, event in enumerate(EVENT_LOG):
        if event['id'] == last_id:
            removed = EVENT_LOG.pop(index)
            print(f"\n Evenimentul '{removed['name']}' anulat.")
            return

    print(f"\n Evenimentul cu ID {last_id} a fost deja procesat.")


def list_events(sort_by: str = 'id'):
    if not EVENT_LOG:
        print("\n Log-ul este gol.")
        return

    sorted_events = sorted(EVENT_LOG, key=lambda x: str(x.get(sort_by)).lower())

    print(f"\n--- Lista Evenimente (Sortate dupa: {sort_by}) ---")
    for e in sorted_events:
        print(f"ID: {e['id']} | Nume: {e['name']} | Prioritate: {e['priority']}")


def main():
    while True:
        print("\n=== Sistem Procesare Evenimente ===")
        print("1. Adauga Eveniment")
        print("2. Proceseaza Urmatorul Eveniment (Queue)")
        print("3. Undo Ultima Adaugare (Stack)")
        print("4. Listeaza Toate Evenimentele")
        print("5. Iesire")

        option = input("Selectati o optiune: ")

        if option == '1':
            name = input("Nume eveniment: ")
            priority = input("Prioritate (LOW, MEDIUM, HIGH)]: ") or 'LOW'
            extra_info = input("Nota aditionala (optional): ")

            if extra_info:
                eid = add_event(name, priority=priority, notes=extra_info)
            else:
                eid = add_event(name, priority=priority)

            push_to_undo(eid)
            print(f"--- Eveniment adaugat cu succes (ID: {eid}) ---")

        elif option == '2':
            process_next_event()
        elif option == '3':
            undo_last_event()
        elif option == '4':
            criterion = input("Sorteaza dupa (id, name, priority) [Default id]: ") or 'id'
            list_events(criterion)
        elif option == '5':
            print("Inchidere aplicatie...")
            break
        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    main()