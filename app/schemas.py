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
    completed: Optional[bool] = False

class TodoItem(TodoItemBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class config:
        orm_mode = True

class UserBase (BaseModel):
    name: str
    email: str
    password: str

class User (BaseModel):
    name: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
