from pydantic import BaseModel, EmailStr

from typing import List, Optional

class UserCreateModel(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str

class LoginModel(BaseModel):
    email : EmailStr
    password : str