import os

from fastapi import UploadFile
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, StorageContext, GPTListIndex, \
    load_index_from_storage, LLMPredictor, PromptHelper, ServiceContext
from llama_index.storage.index_store import MongoIndexStore
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.node_parser import SimpleNodeParser
from .data_access import database

def initialize_context():
    global index
    global storage_context
    index_exists = True

    if index_exists:
        define_storage_context()
    else:
        build_index()

    index = load_index_from_storage(storage_context)

def ask(question: str):
    engine = index.as_query_engine()
    query_result = engine.query(question)

    return query_result.response

async def upload_file(file: UploadFile): 
    complete_path = await write_file(file)

    documents = SimpleDirectoryReader(input_files=[complete_path]).load_data()
    
    index.insert(documents[0], storage_context=storage_context)
    storage_context.persist()

    return {"message:": "File uploaded successfully"}

async def write_file(file: UploadFile):
    save_path = './documents'
    complete_path = os.path.join(save_path, file.filename)

    try:
        contents = await file.read()
        with open(complete_path, 'wb') as f:
            f.write(contents)
    except Exception:
        raise Exception("There was an error uploading the file")
    finally:
        await file.close()
    
    return complete_path


def build_index():
    global index
    global storage_context

    print('Generating new index...')
    documents = SimpleDirectoryReader('./documents').load_data()

    num_outputs = 100
    max_input_size = 100
    max_chunk_overlap = 20

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model='gpt-3.5-turbo'))
    prompt_helper = PromptHelper(max_input_size=max_input_size, num_output=num_outputs, max_chunk_overlap=max_chunk_overlap)

    define_storage_context()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    nodes = SimpleNodeParser().get_nodes_from_documents(documents)
    index = GPTListIndex(nodes, service_context=service_context, storage_context=storage_context)
    storage_context.persist()


def define_storage_context():
    global storage_context

    db_connection_string = database.get_database_connection_string()
    db_name = database.get_database_name()

    index_store = MongoIndexStore.from_uri(db_connection_string, db_name)
    docstore = MongoDocumentStore.from_uri(db_connection_string, db_name)
    storage_context = StorageContext.from_defaults(index_store=index_store, docstore=docstore)