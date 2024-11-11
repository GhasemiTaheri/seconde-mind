from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import Field, BaseModel


class Note(Document):
    title: str
    description: str
    user: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = 'notes'
        use_state_management = True


class PublicNote(BaseModel):
    id: PydanticObjectId
    title: str
    description: str | None
    created_at: datetime


class CreateNote(BaseModel):
    title: str
    description: str | None
