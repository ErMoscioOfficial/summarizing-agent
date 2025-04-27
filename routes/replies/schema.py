from pydantic import BaseModel

class ReplyCreateModel(BaseModel):
    external_id : str
    content : str
    post_id : int