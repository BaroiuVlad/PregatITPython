from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

# All lowercase imports for Linux/Docker compatibility
from db_handler import create_tables
from schemas import TaskCreateRequest, TaskResponse, TaskStatusChangeRequest, TaskUpdateRequest
from task_system import TaskManager
from custom_exceptions import TaskNotFoundError, InvalidInputError, InvalidStatusTransitionError

app = FastAPI(title="Task Management API")
manager = TaskManager()

@app.on_event("startup")
async def startup_event():
    create_tables()

# ... (Keep your format_task and exception handlers here)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateRequest):
    task = manager.create_task(payload.title, payload.owner, payload.description)
    return {
        "id": task._id, "title": task._title, "owner": task._owner,
        "description": task._description, "status": task._status,
        "created_at": task._created_at, "updated_at": task._updated_at,
    }