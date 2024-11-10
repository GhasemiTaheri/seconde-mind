from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from db import init
from web.auth import router as auth_router
from web.user import router as user_router
from web.note import router as note_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(note_router)
