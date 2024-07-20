
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2

from ..database import  get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user:object = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.postid).label("votes")).join(models.Vote, models.Vote.postid == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), user:object = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.postid).label("votes")).join(models.Vote,  models.Vote.postid == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} not found")
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user:object = Depends(oauth2.get_current_user)):
   new_post = models.Post(userid = user.id, **post.model_dump())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post    

@router.put("/{id}",  response_model=schemas.Post)
def update_post(id: int, upost: schemas.PostCreate, db: Session = Depends(get_db), user:object = Depends(oauth2.get_current_user)):
   
    record = db.query(models.Post).filter(models.Post.id == id)
    
    if not record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} not found")
    
    
    if record.first().userid != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"User with id:{user.id} not allowed to update post with id:{id}")
    
    record.update(upost.model_dump(), synchronize_session=False)

    db.commit()
    
    return record.first()  


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),  user:object = Depends(oauth2.get_current_user)):
    
    record = db.query(models.Post).filter(models.Post.id == id)
    
    if record.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} not found")
    
    if record.first().userid != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"User with id:{user.id} not allowed to delete post with id:{id}")
    
    
    record.delete(synchronize_session=False)
    db.commit()
    return f"Deleted successfully post with id:{id}"  
