from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas, models, database
from hashing import Hash


router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def createUser(request:schemas.User, db: Session = Depends(database.get_db)):

    new_user = models.User(name=request.name, email= request.email, password = Hash.bcrypt(request.password))
    # new_user = models.User(request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.ShowUserBlog)
def user(id:int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=' User Not found')
    return user