from sqlmodel import select

from db.models import Channels, Posts
from routes.posts.schema import PostCreateModel, PostDetailModel

from routes.replies.service import ReplyService

from sqlalchemy.ext.asyncio import AsyncSession

reply_service = ReplyService()

class PostService:
    async def get_posts(self, session : AsyncSession):
        stmt = select(Posts)
        data = await session.exec(stmt)
        return data.all()

    async def get_post_by_id(self, id : int, session : AsyncSession):
        stmt = select(Posts).where(Posts.id == id)
        data = await session.exec(stmt)
        return data.first()

    async def get_post_by_id_with_replies(self, id, session):
        post = await self.get_post_by_id(id, session)
        replies = await reply_service.get_replies_for_post(id, session)
        detail_model = PostDetailModel(**post.model_dump())

        return detail_model

    async def get_post_by_channel_id(self, channel_id : int, session: AsyncSession):
        stmt = select(Posts).where(Posts.channel_id == channel_id)
        data = await session.exec(stmt)

        return data.all()

    async def create_post(self, data : PostCreateModel, session : AsyncSession):
        new_post = Posts(**data.model_dump())

        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)

        return new_post