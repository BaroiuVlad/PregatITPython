import time
from db_handler import get_db_connection
from custom_exceptions import (
    InvalidInputError,
    TaskNotFoundError,
    InvalidStatusTransitionError,
    EmptyUndoStackError,
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

class TaskManager:
    def __init__(self):

        self.undo_stack = []

    def create_task(self, title, owner, description=""):
        if not title or not str(title).strip():
            raise InvalidInputError("title", title, "Titlul nu poate fi gol.")
        if not owner or not str(owner).strip():
            raise InvalidInputError("owner", owner, "Responsabilul nu poate fi gol.")

        new_task = Task(title.strip(), owner.strip(), description.strip())
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:

                query = """INSERT INTO tasks (title, description, owner, status, created_at, updated_at) 
                           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"""
                cur.execute(query, (new_task._title, new_task._description, new_task._owner,
                                    new_task._status, new_task._created_at, new_task._updated_at))
                new_task._id = cur.fetchone()["id"]
                conn.commit()
        finally:
            conn.close()
        return new_task

    def list_tasks(self, filter_status=None, filter_owner=None, sort_by="id"):
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        if filter_status:
            query += " AND status = %s"
            params.append(filter_status.upper())
        if filter_owner:
            query += " AND owner = %s"
            params.append(filter_owner)

        allowed_sort = {"id": "id", "owner": "owner", "status": "status", "updated_at": "updated_at"}
        query += f" ORDER BY {allowed_sort.get(sort_by, 'id')}"

        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                return [Task(task_id=r["id"], title=r["title"], owner=r["owner"],
                             description=r["description"], status=r["status"],
                             created_at=r["created_at"], updated_at=r["updated_at"]) for r in rows]
        finally:
            conn.close()

    def get_task_by_id(self, task_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
                row = cur.fetchone()
                if not row:
                    raise TaskNotFoundError(task_id)
                return Task(task_id=row["id"], title=row["title"], owner=row["owner"],
                            description=row["description"], status=row["status"],
                            created_at=row["created_at"], updated_at=row["updated_at"])
        finally:
            conn.close()

    def update_task(self, task_id, title=None, owner=None, description=None):
        task = self.get_task_by_id(task_id)

        new_title = title.strip() if title else task._title
        new_owner = owner.strip() if owner else task._owner
        new_desc = description.strip() if description is not None else task._description
        new_updated_at = time.time()

        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET title = %s, owner = %s, description = %s, updated_at = %s WHERE id = %s",
                    (new_title, new_owner, new_desc, new_updated_at, task_id)
                )
                conn.commit()
        finally:
            conn.close()

    def change_status(self, task_id, new_status):
        task = self.get_task_by_id(task_id)
        current_status = task._status.upper()
        new_status = new_status.upper().strip()

        valid_transitions = {
            "CREATED": ["IN_PROGRESS", "DONE"],
            "IN_PROGRESS": ["DONE", "BLOCKED"],
            "BLOCKED": ["IN_PROGRESS", "DONE"],
            "DONE": [],
        }

        if new_status in valid_transitions.get(current_status, []):
            conn = get_db_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE tasks SET status = %s, updated_at = %s WHERE id = %s",
                        (new_status, time.time(), task_id)
                    )
                    conn.commit()
            finally:
                conn.close()
        else:
            raise InvalidStatusTransitionError(current_status, new_status)

    def delete_task(self, task_id):
        self.get_task_by_id(task_id)
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                conn.commit()
        finally:
            conn.close()