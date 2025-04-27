from pydantic import BaseModel
from datetime import datetime

from typing import List

from db.models import Replies

class PostCreateModel(BaseModel):
    external_id : str
    name : str
    content: str
    channel_id : int

class PostDetailModel(BaseModel):
    id: int
    external_id : str
    name : str
    content: str
    channel_id : int
    created_at : datetime
    replies : List[Replies] = []