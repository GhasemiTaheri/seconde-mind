from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from model import User, Note


async def init() -> None:
    client = AsyncIOMotorClient(str(settings.MONGODB_URI))
    await init_beanie(
        database=getattr(client, settings.MONGODB_DB_NAME),
        document_models=[
            User,
            Note
        ],
    )
