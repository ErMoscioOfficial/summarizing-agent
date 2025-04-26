from fastapi import APIRouter, Depends, status

from routes.summarize.schema import ConversationSummary, SummarizationRequest
from routes.summarize.service import SummarizationService

from db.models import Users
from routes.auth.dependencies import get_current_user

summ_service = SummarizationService()
summ_router = APIRouter()

@summ_router.post('')
async def summarize_request(summarize_request : SummarizationRequest, user : Users = Depends(get_current_user)):
    text = summarize_request.content
    summary = await summ_service.summarize_text(text, user.first_name, user.last_name)
    return summary