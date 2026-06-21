class TaskManagerException(Exception):
    pass


class InvalidInputError(TaskManagerException):
    def __init__(self, field_name: str, value: str, reason: str):
        self.message = (
            f"Valoare invalida pentru campul '{field_name}': '{value}'. Motiv: {reason}"
        )
        super().__init__(self.message)


class TaskNotFoundError(TaskManagerException):
    def __init__(self, task_id: int):
        self.message = (
            f"Eroare: Task-ul cu ID-ul {task_id} nu a fost gasit in baza de date."
        )
        super().__init__(self.message)


class InvalidStatusTransitionError(TaskManagerException):
    def __init__(self, current_status: str, target_status: str):
        self.message = f"Tranzitie interzisa: Nu se poate trece de la {current_status} la {target_status}."
        super().__init__(self.message)


class EmptyUndoStackError(TaskManagerException):
    def __init__(self):
        super().__init__("Stiva de Undo este goala. Nu exista actiuni de anulat.")
