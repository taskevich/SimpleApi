import jwt
import bcrypt
import hashlib

from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security.http import HTTPBase, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status
from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request

from backend.backend.models import Users


ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"


class CustomHTTPBearer(HTTPBase):
    def __init__(
        self,
        *,
        bearerFormat: str = None,
        scheme_name: str = None,
        description: str = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> HTTPAuthorizationCredentials:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


def create_access_token(data: Users):
    to_encode = {
        "id": data.id,
        "username": data.username,
        "password": data.password,
        "email": data.email,
        "phone": data.email,
        "role": {
            "id":  data.role.id,
            "name": data.role.name
        },
        "is_active": data.is_active,
        "is_blocked": data.is_blocked,
        "is_receive_notifications": data.is_receive_notifications
    }
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_password(password: str):
    hashed = hashlib.sha256(password.encode())
    return hashed.hexdigest()


def check_password(password: str, hashed_password: str):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password
