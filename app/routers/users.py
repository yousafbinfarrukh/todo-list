from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import schemas, database, models, oauth2
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/user', 
    tags=['users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def user (request: schemas.UserBase, db: Session = Depends(database.get_db)):
    hasher = Hash()
    new_user = models.User(name=request.name, email=request.email, password=hasher.bcrypt(request.password))
    db.add (new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.User])
def all_user (db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    if len(users) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found')
    return users

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def user(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID={id} not found')
    return user

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def item (id: int, db : Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    item = db.query(models.User).filter(models.User.id == id).delete(synchronize_session='evaluate')
    db.commit()
    return {'detail': 'Deleted'}
