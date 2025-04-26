from pydantic import BaseModel, Field
from typing import List, Optional

class SummarizationRequest(BaseModel):
    channel_name : str
    content : str

class ModelResponse(BaseModel):
    content : str

class MessageItem(BaseModel):
    person: Optional[str] = Field(None, description="Name of the person speaking, if applicable")
    message: str = Field(description="The actual message content")

class ConversationSummary(BaseModel):
    topics_discussed: List[MessageItem] = Field(description="Key topics discussed during the conversation")
    decisions_made: List[MessageItem] = Field(description="Any decisions made during the conversation")
    action_items: List[MessageItem] = Field(description="Action items or next steps identified during the conversation")
    selected_user_items: List[MessageItem] = Field(description="Action items or next steps identified during the conversation that are attributable to me")

