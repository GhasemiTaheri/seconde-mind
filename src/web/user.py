from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from utils.dependencies import get_current_active_user
from model import User, PublicUser, CreateUser
from utils.security import get_password_hash

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=PublicUser, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: CreateUser):
    """Create new user in the database."""
    user = await User.get_by_username(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user associated with this username already exists",
        )
    data = user_in.dict()
    data["hashed_password"] = get_password_hash(data.pop("password"))
    return await User(**data).insert()


@router.get("/me", response_model=PublicUser, status_code=status.HTTP_200_OK)
async def get_current_user(user: Annotated[User, Depends(get_current_active_user)]):
    """Get current active user details."""
    return user
