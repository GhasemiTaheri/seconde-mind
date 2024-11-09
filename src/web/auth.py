from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from model import User
from utils import security

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/access-token",
             description="Generate an access token for the given username and password.")
async def generate_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get an access token for future requests."""
    user = await User.authenticate(username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    expires_in = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return JSONResponse(
        content={
            "access_token": security.create_access_token(user.id, expires_delta=expires_in),
            "token_type": "bearer",
        }
    )
