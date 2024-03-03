import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from backend.backend.auth import CustomHTTPBearer, SECRET_KEY, ALGORITHM
from backend.backend.models import Users
from backend.backend.schemas import *

router = APIRouter()
security = CustomHTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token:
            return Users(id=decoded_token["id"], name=decoded_token["name"], password=decoded_token["password"])
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.get("/panel", response_model=PanelResponse, tags=["API", "PANEL"])
async def panel():
    return PanelResponse()
