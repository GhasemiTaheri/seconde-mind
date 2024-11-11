from typing import Annotated

from fastapi import APIRouter, Depends, status

from utils.dependencies import get_current_active_user
from model import User, PublicUser

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me/", response_model=PublicUser, status_code=status.HTTP_200_OK)
async def get_current_user(user: Annotated[User, Depends(get_current_active_user)]):
    return user
