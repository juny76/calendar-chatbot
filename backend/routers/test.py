from backend.models import ChatRequest, ChatResponse
from backend.usecases import run_agent_executor


chat_request: ChatRequest
chat_request = ChatRequest( user_email = "tuannguyenhuy87@gmail.com",
    user_message= "summary my schedule next week",
    calendar_id = "tuannguyenhuy87@gmail.com")

try:
    answer = run_agent_executor(
        chat_request.user_email, chat_request.user_message, chat_request.calendar_id
    )
    print(answer)
except Exception as e:
    raise print(e)