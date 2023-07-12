from fastapi import UploadFile

from .data_access import files
from .data_access.encoder import MongoJSONEncoder
from datetime import datetime

def ask(question: str):
    return {"answer": f'Question: {question} Answer: Random answer'}

async def upload_file(file: UploadFile):
    files.insert_file({
        'name': file.filename,
        'createdAt': datetime.now()
    })

    return {"message": "File uploaded successfully"}

def initialize_context(): 
    print('Using mock :)')

def get_file(fileId: str):
    return MongoJSONEncoder().encode(files.get_file(fileId))

def get_all_files():
    return MongoJSONEncoder().encode(list(files.get_all_files()))

def delete_file(fileId: str):
    files.delete_file(fileId)
    return {"message": "File deleted successfully"}