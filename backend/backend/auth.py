from fastapi import HTTPException
from fastapi.security.http import HTTPBase, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request


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