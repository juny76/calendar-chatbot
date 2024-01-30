from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
import logging
import os


def connect_to_mongo():
    db_client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
    try:
        return db_client
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

db = client.get_database(os.getenv("DB_NAME"))
