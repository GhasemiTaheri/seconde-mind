from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from model import User, Note
from utils.security import get_password_hash


async def init() -> None:
    client = AsyncIOMotorClient(str(settings.MONGODB_URI))
    await init_beanie(
        database=getattr(client, settings.MONGODB_DB_NAME),
        document_models=[
            User,
            Note
        ],
    )
    if not await User.get_by_username(username=settings.FIRST_SUPERUSER):
        await User(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        ).insert()
