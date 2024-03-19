import jwt
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException
from starlette import status

from backend.backend.auth import create_access_token, check_password, CustomHTTPBearer, ALGORITHM, SECRET_KEY
from backend.backend.schemas import *
from backend.backend.models import *
from backend.backend.auth import hash_password

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


@router.post("/api/auth/login", response_model=AuthResponse, tags=["API", "CREDENTIALS"])
async def login(request: AuthRequest):
    """ Маршрут авторизации """
    username = request.usernameOrEmail
    password = request.password

    user = await DB().get_user_by_username_or_email(username)
    if user.is_blocked:
        return DefaultResponse(error=True, message="Аккаунт не активен")

    if not user:
        return DefaultResponse(error=True, message="Пользователь с таким именем пользователя не найден")

    if check_password(password, user.password) is False:
        return DefaultResponse(error=True, message="Неправильный пароль")

    token = create_access_token(user)

    return AuthResponse(message=token)


@router.post("/api/auth/registration", response_model=RegistrationResponse, tags=["API", "CREDENTIALS"])
async def register(request: RegistrationRequest):
    """ Маршрут регистарции """

    # todo: email verification

    error, message = await DB().create_new_user(username=request.username, password=hash_password(request.password),
                                                email=request.email, phone=request.phone,
                                                receive_notifications_email=request.receiveNotificationsEmail)
    if error is True:
        return RegistrationResponse(error=True, message=message)

    return RegistrationResponse(error=False, message=message)


@router.post("/api/auth/recovery", response_model=RecoveryResponse, tags=["API", "CREDENTIALS"])
async def recovery(request: RecoveryRequest):
    """ Запрос на восстановление аккаунта """

    # todo: send email verification

    username_or_email = request.usernameOrEmail
    new_password = request.newPassword

    error, message = await DB().change_user_data(username_or_email=username_or_email,
                                                 new_password=hash_password(new_password))

    if error is True:
        return RecoveryResponse(error=error, message=message)

    return RecoveryResponse(error=error, message=message)
