from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2

from typing import List

from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users",
                    tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user.password = utils.get_hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/" , response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}" , response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user

# @router.put("/{id}", response_model=schemas.UserOut)
# def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)):
    
#     query = db.query(models.User).filter(models.User.id == id)
    
#     record = query.first()
    
#     if not record:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"User with id:{id} not found")
    
#     query.update(user.model_dump(), synchronize_session=False)

#     db.commit()
    
#     return query.first()


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(id: int, db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)):
    
#     record = db.query(models.User).filter(models.User.id == id)
    
#     if record.first() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"User with id:{id} not found")
    
#     record.delete(synchronize_session=False)
#     db.commit()
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)