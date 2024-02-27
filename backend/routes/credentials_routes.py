from fastapi import APIRouter

from backend.backend.schemas import *

router = APIRouter()


@router.post("/api/auth/login", response_model=AuthResponse, tags=["API", "CREDENTIALS"])
async def login(request: AuthRequest):
    """ Маршрут авторизации """
    return AuthResponse()


@router.post("/api/auth/registration", response_model=RegistrationResponse, tags=["API", "CREDENTIALS"])
async def register(request: RegistrationRequest):
    """ Маршрут регистарции """
    return RegistrationResponse()


@router.post("/api/auth/recovery", response_model=RecoveryResponse, tags=["API", "CREDENTIALS"])
async def recovery(request: RecoveryRequest):
    """ Запрос на восстановление аккаунта """
    return RecoveryResponse()
