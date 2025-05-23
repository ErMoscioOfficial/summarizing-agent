from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Any, List

from db import get_session
from db.models import Users

from errors import (
    AccessTokenRequired,
    InvalidToken
)

from routes.auth.service import AuthService
from routes.auth.utils import decode_token


user_service = AuthService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        print(request.headers)
        creds = await super().__call__(request)

        token = creds.credentials
        print(creds)

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()

async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]
    print(token_details)

    user = await user_service.get_user_by_email(user_email, session)

    return user