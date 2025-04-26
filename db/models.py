from sqlmodel import (
    SQLModel, 
    Field, 
    Relationship, 
    Column
)

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
