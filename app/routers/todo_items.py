from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/todo_items',
    tags=['todo_items']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TodoItem)
def create(request: schemas.TodoItemCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_item = models.TodoItem(
        title=request.title,
        description=request.description,
        owner_id=current_user.id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.TodoItem])
def all(response: Response, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    items = db.query(models.TodoItem).filter(models.TodoItem.owner_id == current_user.id).all()
    return items

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.TodoItem)
def item(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id, models.TodoItem.owner_id == current_user.id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f'Item with id {id} not found')
    return item

@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_item(id: int, request: schemas.TodoItemUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id, models.TodoItem.owner_id == current_user.id)
    if not item.first():
        raise HTTPException(status_code=404, detail=f'Item with id {id} not found')
    item.update(request.dict(exclude_unset=True))
    db.commit()

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_item(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id, models.TodoItem.owner_id == current_user.id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f'Item with id {id} not found')
    db.delete(item)
    db.commit()
    return {'detail': 'Deleted'}