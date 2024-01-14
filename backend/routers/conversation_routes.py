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
from backend.vectorstore.faiss import create_faiss_vector_db

router = APIRouter()


@router.get("/conversations")
def get_conversations(user_email: str):
    db = get_db()
    users = db.get_collection("users")
    conversations = users.find_one({"email": user_email})
    return conversations


@router.get("/conversations/{name}")
def get_conversation(name: str, user_email: str):
    db = get_db()
    users = db.get_collection("users")
    user = users.find_one({"email": user_email})
    conversations = user.get("conversations", [])
    for conversation in conversations:
        if conversation.name == name:
            return conversation


@router.get("/conversations/{name}/get-history")
def get_conversation_history(name: str, user_email: str):
    db = get_db()
    users = db.get_collection("users")
    user = users.find_one({"email": user_email})
    conversations = user.get("conversations", [])
    for conversation in conversations:
        if conversation.name == name:
            return conversation.chat_history


@router.post("/conversations/{name}/chat")
def chat_in_conversation(chat_request: FullChatRequest):
    db = get_db()
    users = db.get_collection("users")
    user = users.find_one({"email": chat_request.user_email})
    conversations = user.get("conversations", [])
    conversation = None
    for conversation in conversations:
        if conversation.name == chat_request.cname:
            conversation = conversation
            break
    chat_history = conversation.chat_history
    llm = create_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are a Education Assistant, use the content in the document to answer the questions.Please answer exactly as shown in the document.If there is no answer in the literature, use your knowledge"
            ),
            MessagesPlaceholder(
                variable_name="chat_history"
            ),
            HumanMessagePromptTemplate.from_template(
                "{human_input}"
            ),
        ]
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    vectorstore = create_faiss_vector_db()
    chat_llm_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}, max_tokens_limit=1024),
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt},
            memory=memory
    )
    result = chat_llm_chain.invoke({"query": chat_request.user_message})
    new_chat_history = ChatHistory(user_email = chat_request.user_email,
                                    timestamp = datetime.now(),
                                    user_input = chat_request.user_message,
                                    ai_response = result.get("result"))
    users.update_one(
        {'email': chat_request.user_email, 'conversations.name': chat_request.cname},
        {'$push': {'conversations.$.chat_history': new_chat_history}}
    )
    return result


