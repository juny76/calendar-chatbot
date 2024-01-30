from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings

from backend.llm.azureopenai import create_embedding

pdf_data_path = ""
vector_db_path = ""

embedding_model = create_embedding()
def create_faiss_vector_db():
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vector_db_path)
    return db

def read_vectors_db():
    db = FAISS.load_local(vector_db_path, embedding_model)
    return db
