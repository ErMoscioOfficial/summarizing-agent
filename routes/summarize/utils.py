from routes.summarize.service import SummarizationService
import asyncio

serv = SummarizationService()

def summarization_wrapper(post_id : int):
    asyncio.run(serv.summarize_text(post_id))