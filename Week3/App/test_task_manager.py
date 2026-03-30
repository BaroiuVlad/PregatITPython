import unittest
import os
from task_system import TaskManager, Task

from db_handler import get_db_connection, create_tables


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Initialize tables before each test
        create_tables()

        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks")
                conn.commit()
        finally:
            conn.close()

        self.manager = TaskManager()

    def test_create_task_db(self):
        task = self.manager.create_task("Test DB", "Vladut", "Descriere")
        self.assertIsNotNone(task._id)

        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tasks WHERE id = %s", (task._id,))
                row = cur.fetchone()

                self.assertEqual(row["title"], "Test DB")
        finally:
            conn.close()

    def test_change_status_persistence(self):
        task = self.manager.create_task("Status Test", "Owner")
        self.manager.change_status(task._id, "IN_PROGRESS")

        updated_task = self.manager.get_task_by_id(task._id)
        self.assertEqual(updated_task._status, "IN_PROGRESS")

    def test_invalid_transition_raises(self):
        from custom_exceptions import InvalidStatusTransitionError

        task = self.manager.create_task("Workflow Test", "Owner")

        with self.assertRaises(InvalidStatusTransitionError):
            self.manager.change_status(task._id, "BLOCKED")
