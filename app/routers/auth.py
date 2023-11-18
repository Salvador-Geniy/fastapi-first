from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
import schemas, models, utils, oauth2
from utils import verify_user_password

auth_router = APIRouter(
    tags=['Authentication']
)


@auth_router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials')
    if not verify_user_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid password')

    data = {"user_id": db_user.id}
    access_token = oauth2.create_access_token(data=data)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Error.')
    return {"access_token": access_token,
            "token_type": "bearer"}
