from pymongo import MongoClient, errors
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MAX_RETRIES = 10
RETRY_DELAY = 5  # seconds

mongodb_uri="mongodb+srv://juny76:tuan762003@cluster0.q4mt3pd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
try:    # The ismaster command is cheap and does not require auth.
    client.admin.command("ping")
    print("connected")
except Exception as err:
    print(f"Could not connect to MongoDB: {err}")



