from datetime import datetime

from pydantic import BaseModel, EmailStr, conint, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(UserCreate):
    pass


class PostBase(BaseModel):
    title: str
    is_published: bool


class PostCreate(PostBase):
    is_published: bool = True


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    author_id: int
    author: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes_count: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str = None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1, ge=0)
