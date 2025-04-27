from sqlmodel import select

from db.models import Channels, Posts
from routes.channels.schema import ChannelCreateModel, ChannelDetailModel

from routes.posts.service import PostService

from sqlalchemy.ext.asyncio import AsyncSession

post_service = PostService()

class ChannelService:
    async def get_channels(self, session : AsyncSession):
        stmt = select(Channels)
        data = await session.exec(stmt)
        return data.all()

    async def get_channel_by_id(self, id : int, session :AsyncSession):
        stmt = select(Channels).where(Channels.id == id)
        data = await session.exec(stmt)
        return data.first()

    async def get_channel_by_id_with_posts(self, id, session):
        channel = await self.get_channel_by_id(id, session)
        posts = await post_service.get_post_by_channel_id(id, session)

        detail_model = ChannelDetailModel(**channel.model_dump(), posts = posts)
        return detail_model


    async def create_channel(self, data : ChannelCreateModel, session : AsyncSession):
        new_channel = Channels(** data.model_dump())

        session.add(new_channel)
        await session.commit()
        await session.refresh(new_channel)

        return new_channel