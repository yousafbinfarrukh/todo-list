from fastapi import FastAPI, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.post('/todoItem', status_code=status.HTTP_201_CREATED, response_model=schemas.TodoItemCreate)
def create (request: schemas.TodoItemCreate, db : Session = Depends(get_db)):
    new_item = models.TodoItem(title=request.title, description=request.description)
    db.add (new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.get('/todoItem', status_code=status.HTTP_200_OK, response_model=list[schemas.TodoItem])
def all (response: Response, db : Session = Depends(get_db)):
    items = db.query(models.TodoItem).all()
    if len(items) == 0:
        raise HTTPException(status_code=404, detail='No Item found')
    return items

@app.get('/todoItem/{id}', status_code=status.HTTP_200_OK, response_model=schemas.TodoItem)
def item (id: int, db : Session = Depends(get_db)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f'Item with {id} not found')
    return item

@app.put('/todoItem/{id}', status_code=status.HTTP_204_NO_CONTENT)
def item (id: int, request: schemas.TodoItemUpdate, db : Session = Depends(get_db)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id)
    if not item.first():
        raise HTTPException(status_code=404, detail=f'Item with {id} not found')
    item.update(request.model_dump(exclude_unset=True))
    db.commit()

@app.delete('/todoItem/{id}', status_code=status.HTTP_200_OK)
def item (id: int, db : Session = Depends(get_db)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id).delete(synchronize_session='evaluate')
    db.commit()
    return {'detail': 'Deleted'}