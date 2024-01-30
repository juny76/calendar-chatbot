from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import os


def create_llm():
    llm = AzureChatOpenAI(model="GPT35TURBO",
                          azure_endpoint=os.environ["API_ENDPOINT"],
                          api_version=os.environ["API_VERSION"],
                          api_key=os.environ["API_KEY"])
    return llm


def create_embedding():
    embedding = AzureOpenAIEmbeddings(
        model="ada",
        azure_endpoint=os.environ["API_ENDPOINT"],
        api_version=os.environ["API_VERSION"],
        api_key=os.environ["API_KEY"]
    )
    return embedding
