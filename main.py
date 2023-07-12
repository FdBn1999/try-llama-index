import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from application import router
from core import logic_factory, config
from fastapi.middleware.cors import CORSMiddleware

os.environ['OPENAI_API_KEY'] = config.get_config('OPENAI_API_KEY')
logic = logic_factory.get_logic()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logic.initialize_context()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router.router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
