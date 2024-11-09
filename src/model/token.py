from beanie import PydanticObjectId
from pydantic import BaseModel


class AuthTokenPayload(BaseModel):
    sub: PydanticObjectId | None = None
