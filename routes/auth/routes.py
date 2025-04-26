from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from db.models import Users
from db import get_session

from errors import UserAlreadyExists, UserNotExists, UserWrongPassword

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from routes.auth.service import AuthService
from routes.auth.schemas import LoginModel, UserCreateModel
from routes.auth.utils import verify_password, create_access_token
from routes.auth.dependencies import get_current_user

auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post('/', response_model = Users)
async def create_user(user_data : UserCreateModel, session : AsyncSession = Depends(get_session)):
    check = await auth_service.get_user_by_email(user_data.email, session)

    if check:
        raise UserAlreadyExists()

    usr = await auth_service.create_account(user = user_data, session = session)

    return usr

@auth_router.post('/login')
async def login(login_data : LoginModel, session : AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    usr = await auth_service.get_user_by_email(email, session)

    if usr is not None:
        if verify_password(password, usr.password):
            usr_data = {
                'user_id':usr.id,
                'first_name':usr.first_name,
                'last_name':usr.last_name,
                'email':usr.email
            }
            at = create_access_token(user_data=usr_data)

            return JSONResponse(
                content = {
                    'message':'Login successful',
                    'access_token':at,
                    'user':usr_data
                }
            )
        else:
            raise UserWrongPassword()
    else:
        raise UserNotExists()

@auth_router.get('/me', response_model = Users)
async def current_user(user : Users = Depends(get_current_user)):
    return user