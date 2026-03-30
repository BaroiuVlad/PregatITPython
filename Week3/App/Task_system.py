import sqlite3
import time
from Db_handler import get_db_connection, create_tables
from Custom_exceptions import (
    InvalidInputError,
    TaskNotFoundError,
    InvalidStatusTransitionError,
    EmptyUndoStackError
)


class Task:
    def __init__(self, title, owner, description="", task_id=None, status="CREATED", created_at=None, updated_at=None):
        self._id = task_id
        self._title = title
        self._owner = owner
        self._description = description
        self._status = status

        self._created_at = created_at if created_at else time.time()
        self._updated_at = updated_at if updated_at else self._created_at

    def format_details(self):

        created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._created_at))
        updated = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._updated_at))

        return (
            f"\n--- Detalii Task [{self._id}] ---\n"
            f"Titlu: {self._title}\n"
            f"Responsabil: {self._owner}\n"
            f"Status: {self._status}\n"
            f"Descriere: {self._description}\n"
            f"Creat la: {created}\n"
            f"Ultima actualizare: {updated}"
        )

    def __str__(self):
        readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._updated_at))
        return f"[{self._id}] {self._title} ({self._status}) - Owner: {self._owner} | Last Update: {readable_time}"


class TaskManager:
    def __init__(self):
        create_tables()
        self.undo_stack = []

    def _save_state_for_undo(self):
        current_tasks = self.list_tasks()

        state_snapshot = [
            {
                "id": t._id, "title": t._title, "owner": t._owner,
                "description": t._description, "status": t._status,
                "created_at": t._created_at, "updated_at": t._updated_at
            } for t in current_tasks
        ]
        self.undo_stack.append(state_snapshot)

    def undo_last_action(self):

        if not self.undo_stack:
            raise EmptyUndoStackError()

        last_state = self.undo_stack.pop()

        with get_db_connection() as conn:

            conn.execute("DELETE FROM tasks")
            query = """INSERT INTO tasks (id, title, description, owner, status, created_at, updated_at) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)"""
            for task_data in last_state:
                conn.execute(query, (
                    task_data["id"], task_data["title"], task_data["description"],
                    task_data["owner"], task_data["status"],
                    task_data["created_at"], task_data["updated_at"]
                ))
            conn.commit()

    def create_task(self, title, owner, description=""):
        if not title or not str(title).strip():
            raise InvalidInputError("Titlul task-ului nu poate fi gol.")
        if not owner or not str(owner).strip():
            raise InvalidInputError("Responsabilul (Owner) nu poate fi gol.")

        new_task = Task(title.strip(), owner.strip(), description.strip())

        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """INSERT INTO tasks (title, description, owner, status, created_at, updated_at) 
                       VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (
                new_task._title, new_task._description, new_task._owner,
                new_task._status, new_task._created_at, new_task._updated_at
            ))
            conn.commit()
            new_task._id = cursor.lastrowid
        return new_task

    def list_tasks(self, filter_status=None, filter_owner=None, sort_by="id"):

        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if filter_status:
            query += " AND status = ?"
            params.append(filter_status.upper())
        if filter_owner:
            query += " AND owner = ?"
            params.append(filter_owner)


        allowed_sort = {"id": "id", "owner": "owner", "status": "status", "updated_at": "updated_at"}
        sort_col = allowed_sort.get(sort_by, "id")
        query += f" ORDER BY {sort_col}"

        with get_db_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [Task(
                task_id=row['id'], title=row['title'], owner=row['owner'],
                description=row['description'], status=row['status'],
                created_at=row['created_at'], updated_at=row['updated_at']
            ) for row in rows]

    def get_task_by_id(self, task_id):
        with get_db_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if not row:
                raise TaskNotFoundError(f"Task-ul cu ID-ul {task_id} nu a fost gasit.")
            return Task(
                task_id=row['id'], title=row['title'], owner=row['owner'],
                description=row['description'], status=row['status'],
                created_at=row['created_at'], updated_at=row['updated_at']
            )

    def update_task(self, task_id, title=None, owner=None, description=None):
        task = self.get_task_by_id(task_id)


        new_title = title.strip() if title else task._title
        new_owner = owner.strip() if owner else task._owner
        new_desc = description.strip() if description is not None else task._description
        new_updated_at = time.time()

        with get_db_connection() as conn:
            conn.execute("""UPDATE tasks SET title = ?, owner = ?, description = ?, updated_at = ? 
                          WHERE id = ?""", (new_title, new_owner, new_desc, new_updated_at, task_id))
            conn.commit()

    def change_status(self, task_id, new_status):
        task = self.get_task_by_id(task_id)
        current_status = task._status.upper()
        new_status = new_status.upper().strip()

        valid_transitions = {
            "CREATED": ["IN_PROGRESS", "DONE"],
            "IN_PROGRESS": ["DONE", "BLOCKED"],
            "BLOCKED": ["IN_PROGRESS", "DONE"],
            "DONE": []
        }

        if new_status in valid_transitions.get(current_status, []):
            with get_db_connection() as conn:
                conn.execute("UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
                             (new_status, time.time(), task_id))
                conn.commit()
        else:
            raise InvalidStatusTransitionError(current_status,new_status)
