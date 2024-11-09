from datetime import datetime

from beanie import Document


class Note(Document):
    title: str
    description: str
    user: int
    created_at: datetime | None
    updated_at: datetime | None
