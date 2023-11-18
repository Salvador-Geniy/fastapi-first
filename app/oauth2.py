from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, models
from database import get_db

from env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()  # make a copy of the data to protect the original data from changes
    expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES or 60

    expire = datetime.utcnow() + timedelta(minutes=int(expires_delta))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Couldn't validate credentials.",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
