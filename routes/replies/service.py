from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from datetime import datetime

from routes.replies.schema import ReplyCreateModel
from db.models import Replies

class ReplyService:
    async def create_reply(self, data : ReplyCreateModel, session : AsyncSession):
        new_reply = Replies(**data.model_dump())

        session.add(new_reply)
        await session.commit()
        await session.refresh(new_reply)
        return new_reply

    async def get_replies_for_post(self, post_id:int, session:AsyncSession):
        stmt = select(Replies).where(Replies.post_id == post_id)

        data = await session.exec(stmt)
        return data.all()

    async def get_new_replies_for_post(self, post_id:int, session:AsyncSession, latest_summary_date : datetime):
        stmt = select(Replies).where(Replies.post_id == post_id).where(Replies.created_at >= latest_summary_date)

        data = await session.exec(stmt)
        return data.all()