from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import create_db_and_tables
from app.features.chat.router import router as chat_router
from app.features.health.router import router as health_router
from app.features.hello.router import router as hello_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="hAlo API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# One line per feature.
app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(hello_router, prefix="/api/hello", tags=["hello"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
