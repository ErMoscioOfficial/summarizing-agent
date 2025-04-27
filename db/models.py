from sqlmodel import (
    SQLModel, 
    Field, 
    Relationship, 
    Column
)

from sqlalchemy import Column, Text

from pydantic import EmailStr

from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import date, datetime

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class Users(SQLModel, table = True, extend_existing = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name : str
    last_name : str
    email : str
    password : str
    role : UserRole
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    class Config:
        extend_existing = True

class Channels(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id : str 
    name : str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    posts : List["Posts"] | None = Relationship(back_populates='channel')

class Posts(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id : str
    name : str
    content: str = Field(sa_column=Column(Text))
    channel_id : Optional[int] = Field(default = None, foreign_key='channels.id')
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    channel : Channels | None = Relationship(back_populates= 'posts')
    replies : List["Replies"] | None = Relationship(back_populates='post')
    summaries : List["Summaries"] | None = Relationship(back_populates='post')

class Replies(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id : str
    content: str = Field(sa_column=Column(Text))
    post_id : Optional[int] = Field(default = None, foreign_key='posts.id')
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    post : Posts | None = Relationship(back_populates='replies')

class Summaries(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    content: str = Field(sa_column=Column(Text))
    post_id : Optional[int] = Field(default = None, foreign_key='posts.id')

    post : Posts | None = Relationship(back_populates='summaries')
