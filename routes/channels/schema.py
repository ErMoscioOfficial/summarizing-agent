from pydantic import BaseModel

from db.models import Posts

from typing import List

from datetime import datetime

class ChannelCreateModel(BaseModel):
    external_id : str
    name : str

class ChannelDetailModel(BaseModel):
    id: int
    external_id : str 
    name : str
    created_at: datetime
    posts : List[Posts] = []