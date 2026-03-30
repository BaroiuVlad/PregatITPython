import unittest
import os
import sqlite3
from Task_system import TaskManager, Task
from Db_handler import DB_NAME, create_tables


class TestTaskManager(unittest.TestCase):
    def setUp(self):

        self.test_db = "test_tasks.db"
        create_tables()
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("DELETE FROM tasks")
            conn.commit()

        self.manager = TaskManager()

    def test_create_task_db(self):

        task = self.manager.create_task("Test DB", "Vladut", "Descriere")
        self.assertIsNotNone(task._id)

        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task._id,)).fetchone()
            self.assertEqual(row['title'], "Test DB")

    def test_change_status_persistence(self):
        task = self.manager.create_task("Status Test", "Owner")
        self.manager.change_status(task._id, "IN_PROGRESS")


        updated_task = self.manager.get_task_by_id(task._id)
        self.assertEqual(updated_task._status, "IN_PROGRESS")

    def test_invalid_transition_raises(self):
        task = self.manager.create_task("Workflow Test", "Owner")
        with self.assertRaises(Exception):  # Sau InvalidStatusTransitionError
            self.manager.change_status(task._id, "BLOCKED")
