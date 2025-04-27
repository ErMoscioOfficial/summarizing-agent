from fastapi import APIRouter, Depends

from routes.auth import get_current_user
from db import get_session
from db.models import Users, Channels, Replies, Posts

from typing import Annotated, List

from sqlalchemy.ext.asyncio import AsyncSession

from routes.replies.schema import ReplyCreateModel
from routes.replies.service import ReplyService

reply_router = APIRouter()
reply_service = ReplyService()

db_dep = Annotated[AsyncSession, Depends(get_session)]
auth = Annotated[Users, Depends(get_current_user)]

@reply_router.post('')
async def create_reply(data : ReplyCreateModel, session : db_dep, user : auth) -> Replies:
    channel = await reply_service.create_reply(data, session)
    return channel