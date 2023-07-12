from fastapi import UploadFile, APIRouter
from fastapi.responses import JSONResponse
from core import logic_factory

router = APIRouter()

logic = logic_factory.get_logic()

@router.get('/ask/{question}')
def ask(question: str):
    return JSONResponse(logic.ask(question))

@router.post('/uploadfile/')
async def upload_file(file: UploadFile):
    return JSONResponse(await logic.upload_file(file))

@router.get('/getfile/{fileId}')
def get_file(fileId: str):
    return JSONResponse(logic.get_file(fileId))

@router.delete('/deletefile/{fileId}')
def delete_file(fileId: str):
    return JSONResponse(logic.delete_file(fileId))

@router.get('/getallfiles')
def get_all_files():
    return JSONResponse(logic.get_all_files())