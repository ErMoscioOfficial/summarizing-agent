from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select
from typing import List

from db.models import Users

from routes.auth.schemas import UserCreateModel
from routes.auth.utils import generate_password_hash

class AuthService:
    async def get_user_by_email(self, email : str, session: AsyncSession) -> Users:
        statement = select(Users).where(Users.email == email)

        res = await session.exec(statement)
        user = res.first()

        return user if user is not None else None

    async def get_user_by_id(self,  user_id : int, session: AsyncSession):
        statement = select(Users).where(Users.id == user_id)

        res = await session.exec(statement)
        user = res.first()

        return user if user is not None else None

    async def create_account(self, user : UserCreateModel, session : AsyncSession):
        user_data = user.model_dump()

        new_user = Users(**user_data)
        new_user.password = generate_password_hash(new_user.password)
        new_user.role = 'user'

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user