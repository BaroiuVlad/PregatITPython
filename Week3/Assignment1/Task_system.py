import json
import os
from datetime import datetime


class Task:
    def __init__(self, title, owner, description="", task_id=None, status="CREATED", created_at=None, updated_at=None):

        self._id = task_id if task_id else int(datetime.now().timestamp())
        self._title = title
        self._owner = owner
        self._description = description
        self._status = status
        self._created_at = created_at if created_at else datetime.now().isoformat()
        self._updated_at = updated_at if updated_at else self._created_at

    def to_dict(self):
        #convertim intr un dictionar pentru fisierul JSON
        return {
            "id": self._id,
            "title": self._title,
            "owner": self._owner,
            "description": self._description,
            "status": self._status,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            title=data["title"],
            owner=data["owner"],
            description=data.get("description", ""),
            task_id=data["id"],
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )

    def __str__(self):

        return f"[{self._id}] {self._title} ({self._status}) - Owner: {self._owner} | Updated: {self._updated_at}"


class TaskManager:
    def __init__(self, filepath="tasks.json"):
        self.filepath = filepath
        self.tasks = []

        self.load_tasks()

    def load_tasks(self):

        if not os.path.exists(self.filepath):
            self.tasks = []
            return

        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        with open(self.filepath, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def create_task(self, title, owner, description=""):
        new_task = Task(title=title, owner=owner, description=description)
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def list_tasks(self, filter_status=None, filter_owner=None, sort_by="id"):
        filtered_tasks = self.tasks


        if filter_status:
            filtered_tasks = [t for t in filtered_tasks if t._status.upper() == filter_status.upper()]
        if filter_owner:
            filtered_tasks = [t for t in filtered_tasks if t._owner.lower() == filter_owner.lower()]


        if sort_by == "id":
            filtered_tasks.sort(key=lambda t: t._id)
        elif sort_by == "owner":
            filtered_tasks.sort(key=lambda t: t._owner)
        elif sort_by == "status":
            filtered_tasks.sort(key=lambda t: t._status)
        elif sort_by == "updated_at":
            filtered_tasks.sort(key=lambda t: t._updated_at)

        return filtered_tasks

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task._id == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, owner=None, description=None):
        task = self.get_task_by_id(task_id)
        if task:
            if title: task._title = title
            if owner: task._owner = owner
            if description is not None: task._description = description

            task._updated_at = datetime.now().isoformat()
            self.save_tasks()
            return True
        return False

    def change_status(self, task_id, new_status):
        task = self.get_task_by_id(task_id)
        if not task:
            return False, "Eroare: Task-ul nu a fost gasit."


        valid_transitions = {
            "CREATED": ["IN_PROGRESS", "DONE"],
            "IN_PROGRESS": ["DONE", "BLOCKED"],
            "BLOCKED": ["IN_PROGRESS", "DONE"],
            "DONE": []
        }

        current_status = task._status.upper()
        new_status = new_status.upper()

        if new_status in valid_transitions.get(current_status, []):
            task._status = new_status
            task._updated_at = datetime.now().isoformat()
            self.save_tasks()
            return True, "Status actualizat cu succes."

        return False, f"Tranzitie invalida din {current_status} in {new_status}."