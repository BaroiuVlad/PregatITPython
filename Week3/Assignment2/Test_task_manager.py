import unittest
import os
from Task_system import TaskManager
from Custom_exceptions import (
    InvalidInputError,
    TaskNotFoundError,
    InvalidStatusTransitionError,
    EmptyUndoStackError
)


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # a temporary folder for the data
        self.test_filepath = "test_tasks_temp.json"
        self.manager = TaskManager(filepath=self.test_filepath)
        # We make sure it s empty everytime we make a test.
        self.manager.tasks = []
        self.manager.undo_stack = []
        self.manager.save_tasks()

    def tearDown(self):
        # we clean the folder after every test
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)

    def test_create_task_success(self):
        task = self.manager.create_task("Test Title", "Test Owner", "Test Desc")
        self.assertEqual(task._status, "CREATED")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertIsNotNone(task._id)

    def test_update_task_success(self):
        task = self.manager.create_task("T1", "O1")
        old_updated_at = task._updated_at

        self.manager.update_task(task._id, title="T2", owner="O2")

        updated_task = self.manager.get_task_by_id(task._id)
        self.assertEqual(updated_task._title, "T2")
        self.assertEqual(updated_task._owner, "O2")
        self.assertNotEqual(updated_task._updated_at, old_updated_at)

    def test_change_status_valid_transition(self):
        task = self.manager.create_task("T", "O")
        self.manager.change_status(task._id, "IN_PROGRESS")
        self.assertEqual(task._status, "IN_PROGRESS")

    def test_list_tasks_filtering(self):
        self.manager.create_task("T1", "O1")
        self.manager.create_task("T2", "O2")
        self.manager.change_status(1, "IN_PROGRESS")

        in_progress_tasks = self.manager.list_tasks(filter_status="IN_PROGRESS")
        self.assertEqual(len(in_progress_tasks), 1)
        self.assertEqual(in_progress_tasks[0]._title, "T1")

    def test_save_and_load_persistence(self):
        self.manager.create_task("Persist", "Owner")


        new_manager = TaskManager(filepath=self.test_filepath)
        self.assertEqual(len(new_manager.tasks), 1)
        self.assertEqual(new_manager.tasks[0]._title, "Persist")

    def test_undo_action_success(self):
        task = self.manager.create_task("T", "O")
        self.manager.change_status(task._id, "IN_PROGRESS")
        self.assertEqual(self.manager.tasks[0]._status, "IN_PROGRESS")

        self.manager.undo_last_action()
        self.assertEqual(self.manager.tasks[0]._status, "CREATED")



    def test_create_task_empty_title_raises(self):
        with self.assertRaises(InvalidInputError):
            self.manager.create_task("", "Owner")

    def test_create_task_empty_owner_raises(self):
        with self.assertRaises(InvalidInputError):
            self.manager.create_task("Title", "   ")

    def test_update_nonexistent_task_raises(self):
        with self.assertRaises(TaskNotFoundError):
            self.manager.update_task(999, title="New Title")

    def test_change_status_invalid_transition_raises(self):
        task = self.manager.create_task("T", "O")
        with self.assertRaises(InvalidStatusTransitionError):
            self.manager.change_status(task._id, "BLOCKED")

    def test_undo_empty_stack_raises(self):
        with self.assertRaises(EmptyUndoStackError):
            self.manager.undo_last_action()

    def test_load_corrupted_json_does_not_crash(self):
        with open(self.test_filepath, 'w') as f:
            f.write("{ invalid_json_format")

        new_manager = TaskManager(filepath=self.test_filepath)
        self.assertEqual(len(new_manager.tasks), 0)


if __name__ == '__main__':
    unittest.main()