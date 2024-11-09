import re
from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import EmailStr, BaseModel
from pydantic.fields import Field

from utils.security import verify_password


class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def get_by_username(cls, *, username: str) -> Optional["User"]:
        return await cls.find_one(cls.username == username.lower())

    @classmethod
    async def get_by_api_key(cls, *, api_key: str) -> Optional["User"]:
        return await cls.find_one(cls.api_key == api_key.lower())

    @classmethod
    async def authenticate(
            cls,
            *,
            username: str,
            password: str,
    ) -> Optional["User"]:
        user = await cls.get_by_username(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    class Settings:
        name = "users"
        use_state_management = True


class PublicUser(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime


class CreateUser(BaseModel):
    username: str = Field(min_length=3,
                          max_length=64,
                          pattern=re.compile(r"^[A-Za-z0-9-_.]+$"),
                          to_lower=True,
                          strip_whitespace=True)
    email: EmailStr
    password: str = Field(min_length=8)
