from core import config

from pymongo import MongoClient

def get_database():
    client = MongoClient(get_database_connection_string())
    return client[get_database_name()]

def get_database_connection_string():
    return config.get_config('CONNECTION_STRING')

def get_database_name():
    return config.get_config('DB_NAME')

def get_file_collection():
    db = get_database()
    return db['files']