from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import Field, BaseModel


class Note(Document):
    title: str
    description: str
    user: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def user_note_list(cls, *, user_id: str) -> Optional["Note"]:
        return await cls.find(cls.user == user_id).to_list()


class PublicNote(BaseModel):
    id: PydanticObjectId
    title: str
    description: str | None
    created_at: datetime


class CreateNote(BaseModel):
    title: str
    description: str | None
