from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    author = relationship("User")


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False, primary_key=True)
    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     nullable=False, primary_key=True)
