from fastapi import APIRouter, Depends

from routes.auth import get_current_user
from db import get_session
from db.models import Users, Channels, Replies, Posts, Summaries

from typing import Annotated, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from routes.posts.schema import PostCreateModel, PostDetailModel
from routes.posts.service import PostService

from routes.summarize.service import SummarizationService

from errors import NoSummariesExist

post_router = APIRouter()

post_service = PostService()
summ_service = SummarizationService()

db_dep = Annotated[AsyncSession, Depends(get_session)]
auth = Annotated[Users, Depends(get_current_user)]

@post_router.get('')
async def get_posts(session : db_dep, user : auth) -> List[Posts]:
    channels = await post_service.get_posts(session)
    return channels

@post_router.get('/{id}')
async def get_post_by_id(id : int, session : db_dep, user : auth) -> Posts:
    channel = await post_service.get_post_by_id(id = id, session = session)
    return channel

@post_router.get('/{id}/replies')
async def get_post_by_id_with_replies(id : int, session : db_dep, user : auth) -> PostDetailModel:
    channel = await post_service.get_post_by_id_with_replies(id, session)
    return channel

@post_router.get('/{id}/latest-summary')
async def get_latest_summary_for_post(id : int, session : db_dep, user : auth) -> Optional[Summaries]:
    summary = await summ_service.get_latest_summary_for_post(id, session)

    if summary is None:
        raise NoSummariesExist()
    return summary

@post_router.get('/{id}/summaries')
async def get_summaries_for_post(id : int, session : db_dep, user : auth) -> List[Summaries]:
    summaries = await summ_service.get_summaries_for_post(id, session)

    if len(summaries) == 0:
        raise NoSummariesExist()
    return summaries

@post_router.post('')
async def create_post(data : PostCreateModel, session : db_dep, user : auth) -> Posts:
    channel = await post_service.create_post(data, session)
    return channel