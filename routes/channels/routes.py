from fastapi import APIRouter, Depends

from routes.auth import get_current_user
from db import get_session
from db.models import Users, Channels

from typing import Annotated, List

from sqlalchemy.ext.asyncio import AsyncSession

from routes.channels.schema import ChannelCreateModel, ChannelDetailModel
from routes.channels.service import ChannelService

channel_router = APIRouter()
channel_service = ChannelService()

db_dep = Annotated[AsyncSession, Depends(get_session)]
auth = Annotated[Users, Depends(get_current_user)]

@channel_router.get('')
async def get_channels(session : db_dep, user : auth) -> List[Channels]:
    channels = await channel_service.get_channels(session)
    return channels

@channel_router.get('/{id}')
async def get_channel_by_id(id : int, session : db_dep, user : auth) -> Channels:
    channel = await channel_service.get_channel_by_id(id = id, session = session)
    return channel

@channel_router.get('/{id}/posts')
async def get_channel_by_id_with_posts(id : int, session : db_dep, user : auth) -> ChannelDetailModel:
    channel = await channel_service.get_channel_by_id_with_posts(id, session)
    return channel

@channel_router.post('')
async def create_channel(data : ChannelCreateModel,session : db_dep, user : auth) -> Channels:
    channel = await channel_service.create_channel(data, session)
    return channel