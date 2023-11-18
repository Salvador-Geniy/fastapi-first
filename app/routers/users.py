from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
import schemas
from database import get_db
from utils import get_password_hash

user_router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@user_router.post('/add', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def register_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Function for create a new user and save to database"""
    clear_password = user.password

    # Converting clear password to hash with hashlib library
    # hashed_password = convert_password_to_hash(clear_password)

    # Converting user password to hash using recommended passlib library
    hashed_password = get_password_hash(clear_password)
    user.password = hashed_password

    # Creating a new user and saving to database
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@user_router.get('/list', response_model=list[schemas.UserOut])
async def get_all_users(db: Session = Depends(get_db)):
    """Function for get list of all users from database"""
    users = db.query(models.User).all()
    return users


@user_router.get('/{user_id}', response_model=schemas.UserOut)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Function for get user by user id"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {user_id} was not found.')
    return user
