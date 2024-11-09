from typing import Optional, cast

from beanie import PydanticObjectId
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from model import AuthTokenPayload, User
from config import settings

bearer_token = OAuth2PasswordBearer(
    tokenUrl="/auth/access-token",
    auto_error=False,
)


async def authenticate_bearer_token(token: str) -> User | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        data = AuthTokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from None
    else:
        return await User.get(cast(PydanticObjectId, data.sub))


async def get_current_user(token: Optional[str] = Depends(bearer_token)) -> User:
    """Gets the current user from the database."""
    user = None
    if token:
        user = await authenticate_bearer_token(token)
    else:
        # This is the exception that is raised by the Depends() call
        # when the user is not authenticated and auto_error is True.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Gets the current active user from the database."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user
