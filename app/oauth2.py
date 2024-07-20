import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from . import schemas, database, models,config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = config.settings.secret_key

ALGORITHM = config.settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payLoad = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: str = payLoad.get("user_id")
        
        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(user_id=user_id)
    
    except jwt.PyJWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    user =  db.query(models.User).filter(models.User.email == token.user_id).first()
    
    
    return user