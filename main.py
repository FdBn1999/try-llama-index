import os

from fastapi import FastAPI, UploadFile
from langchain import OpenAI
from contextlib import asynccontextmanager
from llama_index import SimpleDirectoryReader, StorageContext, GPTListIndex, \
    load_index_from_storage, LLMPredictor, PromptHelper, ServiceContext
from llama_index.storage.index_store import MongoIndexStore
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.node_parser import SimpleNodeParser
from dotenv import dotenv_values

config = dotenv_values()

os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']

@asynccontextmanager
async def lifespan(app: FastAPI):
    global index
    global storage_context

    index_exists = True

    if index_exists:
        define_storage_context()
    else:
        build_index()

    index = load_index_from_storage(storage_context)

    yield

app = FastAPI(lifespan=lifespan)

@app.get('/ask/{question}')
def ask(question: str):
    print(question)

    engine = index.as_query_engine()
    query_result = engine.query(question)

    return query_result.response

@app.post('/uploadfile/')
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

    num_outputs = 256
    max_input_size = 4096
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
    index_store = MongoIndexStore.from_uri(config['CONNECTION_STRING'], db_name=config['DB_NAME'])
    docstore = MongoDocumentStore.from_uri(config['CONNECTION_STRING'], db_name=config['DB_NAME'])
    storage_context = StorageContext.from_defaults(index_store=index_store, docstore=docstore)
    