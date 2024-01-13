from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
import logging


def connect_to_mongo():


    mongodb_uri = "mongodb+srv://juny76:tuan762003@cluster0.q4mt3pd.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
    try:
        return client
    except Exception as err:
        print(f"Could not connect to MongoDB: {err}")
        return None


MAX_RETRIES = 10
RETRY_DELAY = 5  # seconds
client = None
for _ in range(MAX_RETRIES):
    client = connect_to_mongo()
    if client:
        break
    print(f"Failed to connect. Retrying in {RETRY_DELAY} seconds...")
    time.sleep(RETRY_DELAY)

if not client:
    raise RuntimeError("Max retries reached. Could not connect to MongoDB.")

print("Connected to MongoDB successfully.")

db = client.get_database("calendar")
