from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2

from typing import List

from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vote",
                    tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user:object = Depends(oauth2.get_current_user)):
    user_id = user.id
    post_id = vote.postid
    vote_dir = vote.vote
    
    query = db.query(models.Vote).filter(models.Vote.userid == user_id, models.Vote.postid == post_id)
    record = query.first()
    
    if record:
        if vote_dir == 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vote already exists")
        if vote_dir == 0:
            query.delete(synchronize_session=False)
            db.commit()
            return {"message":"Vote removed"}
    else:
        new_vote = models.Vote(postid = post_id, userid = user_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return f"new vote added {user_id, post_id}"
    
    
# @router.get("/" , response_model=List[schemas.UserOut])
# def get_users(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users

# @router.get("/{id}" , response_model=schemas.UserOut)
# def get_user(id:int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     return user