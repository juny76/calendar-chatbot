from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings


def create_llm():
    llm = AzureChatOpenAI(model="GPT35TURBO",
                          azure_endpoint="https://sunhackathon1.openai.azure.com/",
                          api_version="2023-07-01-preview",
                          api_key="01996b13c3d44a149d98031a1327715d")
    return llm


def create_embedding():
    embedding = AzureOpenAIEmbeddings(
        model="ada",
        azure_endpoint="https://sunhackathon1.openai.azure.com/",
        api_version="2023-05-15",
        api_key="01996b13c3d44a149d98031a1327715d"
    )
    return embedding
