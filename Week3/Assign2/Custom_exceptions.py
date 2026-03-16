class TaskManagerException(Exception):

    pass

class InvalidInputError(TaskManagerException):
    """we throw this exception when the input is invalid."""
    pass

class TaskNotFoundError(TaskManagerException):
    """we throw this when there is not an ID"""
    pass

class InvalidStatusTransitionError(TaskManagerException):
    """Thrown when an attempt is made to perform a workflow status transition that is not allowed."""
    pass

class EmptyUndoStackError(TaskManagerException):
    """Thrown when an Undo is attempted but the undo stack is empty."""
    pass