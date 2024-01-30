from fastapi import APIRouter, HTTPException
<<<<<<< HEAD
from backend.llm_agent import run_agent_executor
=======

from backend.dependencies import get_db
from backend.usecases import run_agent_executor
>>>>>>> 6640f2335eef9a704365f9164ece96e9f6a99663
from backend.models import ChatRequest,ChatResponse

router = APIRouter()


@router.post("")
def get_calendars_list(chat_request: ChatRequest):
    db = get_db().client.get_database("calendar")
    try:
        answer = run_agent_executor(
            chat_request.user_email, chat_request.user_message, chat_request.calendar_id
        )
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
