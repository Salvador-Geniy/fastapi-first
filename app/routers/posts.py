from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

import models, oauth2, schemas

from database import get_db


post_router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@post_router.get('/list', response_model=list[schemas.PostOut])
async def get_all_posts(db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user),
                        limit: int = 20,
                        offset: int = 0,
                        search: Optional[str] = ""):
    """Function for get list of all posts"""
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(offset).all()
    return posts


@post_router.get('/own_posts', response_model=list[schemas.PostOut])
async def get_all_own_posts(db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    """Function for get list of own posts only"""
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.author_id == current_user.id).all()
    return posts


@post_router.post('/add', response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def add_post(post: schemas.PostCreate,
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    """Function for create a new post"""
    new_post = models.Post(author_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@post_router.get('/{post_id}', response_model=schemas.PostOut)
async def get_post_by_id(post_id: int,
                         db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user)):
    """Function for get post by post id"""
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    print(f"post: {post}")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {post_id} was not found.')
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
    return post


@post_router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(post_id: int,
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    """Function for delete post by post id"""
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {post_id} was not found.')
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
    post_query.delete(synchronize_session=False)
    db.commit()


@post_router.put('/{post_id}', response_model=schemas.Post)
def update_post_by_id(post_id: int,
                      post_data: schemas.PostUpdate,
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    """Function for update post by post id"""
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {post_id} was not found.')
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# Old connection to database
# from database_connect import connect_to_database
# cursor, conn = connect_to_database()

# Method with simple SQL-query inside
# @post_router.get('/')
# def get_all_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"data": posts}
