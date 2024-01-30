import datetime

from fastapi import APIRouter, HTTPException
from datetime import datetime
from backend.dependencies import get_db
from backend.models.chat import FullChatRequest
from backend.usecases import run_agent_executor
from backend.models import ChatRequest, ChatResponse

router = APIRouter()


@router.post("new-chat/create")
def create_new_chat(user_email: str):
    db = get_db().client.get_database("calendar")
    cname = "new-chat" + datetime.now().strftime("%Y%m%d%H%M%S")
    dt = datetime.now()
    result = db.get_database("calendar").get_collection("users").update_one(
        {"email": user_email},
        {"$push": {"conversations": {"name": cname, "timestamp": dt, "chat_history": []}}}
    )
    return result.modified_count > 0



