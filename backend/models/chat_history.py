from datetime import datetime

from pydantic import BaseModel


class ChatHistory(BaseModel):
    user_email: str
    timestamp: str
    user_input: str
    ai_response: str
