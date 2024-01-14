from datetime import datetime
from typing import List

from pydantic import BaseModel

from backend.models.chat_history import ChatHistory


class Conversation(BaseModel):
    name: str
    timestamp: datetime
    chat_history: List[ChatHistory]


class UserRequest(BaseModel):
    user_email: str
