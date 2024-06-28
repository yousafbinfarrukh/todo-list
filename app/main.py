from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.post('/todoItem', status_code=status.HTTP_201_CREATED, response_model=schemas.TodoItemBase)
def create (request: schemas.TodoItem, db : Session = Depends(get_db)):
    new_item = models.TodoItem(title=request.title, description=request.description)
    db.add (new_item)
    db.commit()
    db.refresh(new_item)
    return new_item