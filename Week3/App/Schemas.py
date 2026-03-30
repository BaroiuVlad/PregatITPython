from pydantic import BaseModel, Field
from typing import Optional

# What a user sends to create a task
class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    description: Optional[str] = ""

# What a user sends to update a task (all fields optional)
class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    owner: Optional[str] = None
    description: Optional[str] = None

# What a user sends to change status
class TaskStatusChangeRequest(BaseModel):
    new_status: str

# How a task looks when sent back to the user
class TaskResponse(BaseModel):
    id: int
    title: str
    owner: str
    description: str
    status: str
    created_at: float
    updated_at: float

    class Config:
        from_attributes = True