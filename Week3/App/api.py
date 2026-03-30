from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional

from Task_system import TaskManager
from Schemas import (
    TaskCreateRequest,
    TaskResponse,
    TaskUpdateRequest,
    TaskStatusChangeRequest
)
from Custom_exceptions import (
    TaskNotFoundError,
    InvalidInputError,
    InvalidStatusTransitionError
)

app = FastAPI(title="Task Management API")
manager = TaskManager()



def format_task(task):
    return {
        "id": task._id,
        "title": task._title,
        "owner": task._owner,
        "description": task._description,
        "status": task._status,
        "created_at": task._created_at,
        "updated_at": task._updated_at
    }



@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InvalidInputError)
async def invalid_input_handler(request: Request, exc: InvalidInputError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(InvalidStatusTransitionError)
async def status_error_handler(request: Request, exc: InvalidStatusTransitionError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


# --- Endpoints ---

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreateRequest):
    task = manager.create_task(payload.title, payload.owner, payload.description)
    return format_task(task)


@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(status: Optional[str] = None, owner: Optional[str] = None, sort_by: str = "id"):
    tasks = manager.list_tasks(filter_status=status, filter_owner=owner, sort_by=sort_by)
    return [format_task(t) for t in tasks]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = manager.get_task_by_id(task_id)
    return format_task(task)


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdateRequest):
    if all(v is None for v in [payload.title, payload.owner, payload.description]):
        raise HTTPException(status_code=400, detail="Provide at least one field to update")

    manager.update_task(task_id, payload.title, payload.owner, payload.description)
    return format_task(manager.get_task_by_id(task_id))


@app.post("/tasks/{task_id}/status", response_model=TaskResponse)
def change_status(task_id: int, payload: TaskStatusChangeRequest):
    manager.change_status(task_id, payload.new_status)
    return format_task(manager.get_task_by_id(task_id))