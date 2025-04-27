from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from routes.summarize.schema import ConversationSummary, SummarizationRequest, ModelResponse
from routes.summarize.service import SummarizationService
from routes.summarize.utils import summarization_wrapper

from db.models import Users, Summaries
from db import get_session
from routes.auth.dependencies import get_current_user

from db.redis import summarize_queue

summ_service = SummarizationService()
summ_router = APIRouter()

@summ_router.post('/post/{post_id}')
async def summarize_request(post_id : int, user : Users = Depends(get_current_user)):
    #summary = await summ_service.summarize_text(session = session, post_id = post_id)
    job = summarize_queue.enqueue(summarization_wrapper, post_id)
    return {"job_id": job.id, "status": "Job enqueued"}
