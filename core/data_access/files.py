from . import database
from bson import ObjectId

files = database.get_file_collection()

def insert_file(file):
    return files.insert_one(file)

def delete_file(fileId):
    return files.delete_one({'_id' : ObjectId(fileId)})

def get_all_files():
    return files.find({})

def get_file(fileId):
    return files.find_one({'_id': ObjectId(fileId)})