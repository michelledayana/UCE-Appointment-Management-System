from pymongo import MongoClient
from app.config import MONGO_URI, MONGO_DB_NAME

_client = None


def get_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def get_services_collection():
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    return db["services"]
