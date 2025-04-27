from db.models import Summaries
from db import get_session

from datetime import datetime

from routes.summarize.schema import ConversationSummary, ModelResponse
from routes.summarize.chain import summarization_chain

from routes.replies.service import ReplyService

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from errors import NoDataToSummarize

reply_service = ReplyService()

class SummarizationService:
    async def summarize_text(self, post_id : int) -> Summaries:
        async for session in get_session():
            latest_summary = await self.get_latest_summary_for_post(post_id, session)

            latest_summary_contents = latest_summary.content if latest_summary is not None else 'No previous context is present'
            latest_summary_date = latest_summary.created_at if latest_summary is not None else datetime(2000,1,1)
            new_messages = await reply_service.get_new_replies_for_post(post_id = post_id, session = session, latest_summary_date = latest_summary_date)

            if len(new_messages) == 0:
                raise NoDataToSummarize()

            model_output = await summarization_chain.arun(
                previous_summary = latest_summary_contents,
                new_messages = '\n'.join([i.content for i in new_messages])
            )

            log = await self.log_summary(post_id, model_output, session)
            
        return log

    async def get_latest_summary_for_post(self, post_id, session : AsyncSession):
        stmt = select(Summaries).where(Summaries.post_id == post_id).order_by(Summaries.created_at.desc()).limit(1)
        data = await session.exec(stmt)
        return data.first()

    async def get_summaries_for_post(self, post_id, session:AsyncSession):
        stmt = select(Summaries).where(Summaries.post_id == post_id)
        data = await session.exec(stmt)
        return data.all()

    async def log_summary(self, post_id : int, contents : str, session : AsyncSession):
        summ = Summaries(post_id = post_id, content = contents)

        session.add(summ)
        await session.commit()
        await session.refresh(summ)

        return summ

