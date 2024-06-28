from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoItemBase (BaseModel):
    title: str
    description: Optional[str] = None

class TodoItemCreate (TodoItemBase):
    pass

class TodoItemUpdate (BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[str] = None

class TodoItem(TodoItemBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime