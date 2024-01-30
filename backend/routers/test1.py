import json
from datetime import datetime

from fastapi import APIRouter
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.chains import ConversationalRetrievalChain, StuffDocumentsChain, LLMChain, RetrievalQA
from backend.dependencies import get_db
from backend.llm.azureopenai import create_llm
from backend.models import chat_history
from backend.models.chat import FullChatRequest
from langchain.chains.question_answering import load_qa_chain

from backend.models.chat_history import ChatHistory
from backend.vectorstore.faiss import read_vectors_db

# from backend.vectorstore.faiss import create_faiss_vector_db

router = APIRouter()

def get_conversations(user_email: str):
    db = get_db()
    users = db.get_collection("users")
    conversations = users.find_one({"email": user_email}).get("conversations")
    return conversations

def create_new_chat(user_email: str):
    db = get_db()
    cname = "new-chat" + datetime.now().strftime("%Y%m%d%H%M%S")
    dt = datetime.now()
    result = db.get_collection("users").update_one(
        {"email": user_email},
        {"$push": {"conversations": {"name": cname, "timestamp": dt, "chat_history": []}}}
    )
    return result.modified_count > 0


def get_conversation(name: str, user_email: str):
    db = get_db()
    users = db.get_collection("users")
    user = users.find_one({"email": user_email})
    conversations = user.get("conversations", [])
    for conversation in conversations:
        if conversation["name"] == name:
            return conversation



def get_conversation_history(name: str, user_email: str):
    db = get_db()
    users = db.get_collection("users")
    user = users.find_one({"email": user_email})
    conversations = user.get("conversations", [])
    for conversation in conversations:
        if conversation['name'] == name:
            return conversation['chat_history']



def chat_in_conversation(chat_request: FullChatRequest):
    llm = create_llm()
    db = get_db()
    users = db.get_collection("users")
    user = users.find_one({"email": chat_request.user_email})
    conversations = user.get("conversations", [])
    conversation = None
    for conversation in conversations:
        if conversation['name'] == chat_request.cname:
            conversation = conversation
            break
    chat_history = conversation['chat_history']
    if chat_history is None: chat_history = [{"user_email": "user","timestamp": datetime.now(),"user_input": " ","ai_response": " "}]
    template = """
You help everyone by answering questions, and improve your answers from previous answers in History.
Don't try to make up an answer, if you don't know, just say that you don't know.
Answer in the same language the question was asked.
Answer in a way that is easy to understand.
Do not say "Based on the information you provided, ..." or "I think the answer is...". Just answer the question directly in detail.

History: {{chat_history}}
 ===========
 Context : {context}
 ===========
Question: {{question}}
=========
{{human_input}}
Answer: 
"""
    PROMPT = PromptTemplate(
        template=template,
        input_variables=["chat_history", "question", "human_input"]
    )

    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,input_key="human_input")
    vectorstore = read_vectors_db()
    chat_llm_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}, max_tokens_limit=1024),
            return_source_documents=False,
            chain_type_kwargs={"prompt": PROMPT},
            # memory=memory
    )

    result = chat_llm_chain.invoke({"query":chat_request.user_message, "question": chat_request.user_message,"chat_history": chat_history, "human_input": chat_request.user_message })
    new_chat_history_dict = {
        "user_email": chat_request.user_email,
        "timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "user_input": chat_request.user_message,
        "ai_response": result.get("result"),
    }
    users.update_one(
        {'email': chat_request.user_email, 'conversations.name': chat_request.cname},
        {'$push': {'conversations.$.chat_history': new_chat_history_dict}}
    )
    return result

user_email = "tuannguyenhuy87@gmail.com"

#[{'name': 'new-chat20240114012740', 'timestamp': datetime.datetime(2024, 1, 14, 1, 27, 40, 372000), 'chat_history': []}]
# print(create_new_chat(user_email))
print(get_conversations(user_email))
print(get_conversation("new-chat20240114012740",user_email))
chat_request = FullChatRequest(user_email = user_email,
                               user_message = "What is VietNam Party?",
                               cname = "new-chat20240114012740")
chat_in_conversation(chat_request)
print(get_conversation_history("new-chat20240114012740",user_email))




