from fastapi import FastAPI
from . import models
from .database import engine
from .routers import todo_items, users

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(todo_items.router)
app.include_router(users.router)


