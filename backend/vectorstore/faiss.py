from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings

pdf_data_path = "D:/code py/time-chatbot/calendar-chatbot/backend/data"
vector_db_path = "D:/code py/time-chatbot/calendar-chatbot/backend/vectorstore/db_faiss"


def create_faiss_vector_db():
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    embedding_model = AzureOpenAIEmbeddings(
        model="ada",
        azure_endpoint="https://sunhackathon1.openai.azure.com",
        api_version="2023-05-15",
        api_key="01996b13c3d44a149d98031a1327715d"
    )
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vector_db_path)
    return db

def read_vectors_db():
    # Embedding
    embedding_model = AzureOpenAIEmbeddings(
        model="ada",
        azure_endpoint="https://sunhackathon1.openai.azure.com",
        api_version="2023-05-15",
        api_key="01996b13c3d44a149d98031a1327715d"
    )
    db = FAISS.load_local(vector_db_path, embedding_model)
    return db
