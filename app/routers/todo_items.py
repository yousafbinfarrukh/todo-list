from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/todo_items', 
    tags=['todo_items']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TodoItemCreate)
def create (request: schemas.TodoItemCreate, db : Session = Depends(database.get_db)):
    new_item = models.TodoItem(title=request.title, description=request.description)
    db.add (new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get('/todoItem', status_code=status.HTTP_200_OK, response_model=list[schemas.TodoItem])
def all (response: Response, db : Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    items = db.query(models.TodoItem).all()
    if len(items) == 0:
        raise HTTPException(status_code=404, detail='No Item found')
    return items


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.TodoItem)
def item (id: int, db : Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f'Item with {id} not found')
    return item

@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def item (id: int, request: schemas.TodoItemUpdate, db : Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id)
    if not item.first():
        raise HTTPException(status_code=404, detail=f'Item with {id} not found')
    item.update(request.model_dump(exclude_unset=True))
    db.commit()

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def item (id: int, db : Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id).delete(synchronize_session='evaluate')
    db.commit()
    return {'detail': 'Deleted'}