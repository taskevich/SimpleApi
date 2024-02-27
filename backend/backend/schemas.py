from typing import Optional, Any, List
from pydantic import BaseModel


class DefaultResponse(BaseModel):
    """ Стандартный ответ на запрос """
    error: Optional[bool] = False
    message: Optional[str] = "OK"
    payload: Optional[Any] = None


class AuthRequest(BaseModel):
    """ Запрос на авторизацию """
    username: Optional[str]
    password: Optional[str]


class AuthResponse(DefaultResponse):
    """ Ответ на запрос авторизации """


class RegistrationRequest(BaseModel):
    """ Запрос на регистрацию """
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
    phone: Optional[str] = None
    receiveNotificationsEmail: Optional[bool] = False


class RegistrationResponse(BaseModel):
    """ Ответ на запрос регистрации """


class RecoveryRequest(DefaultResponse):
    """ Запрос на восстановление аккаунта """
    username: Optional[str]
    email: Optional[str] = None
    newPassword: Optional[str]


class RecoveryResponse(DefaultResponse):
    """ Ответ на восстановление аккаунта """


class FeatureElement(BaseModel):
    """ Элемент фичи """
    name: Optional[str]


class DiscountElement(BaseModel):
    """ Элемент скидки """
    name: Optional[str]
    value: Optional[float]


class TariffItem(BaseModel):
    """ Элемент тарифа """
    name: Optional[str]
    description: Optional[str]
    discount: Optional[DiscountElement] = None
    price: Optional[str] = None
    features: Optional[List[FeatureElement]] = None


class TariffsResponse(DefaultResponse):
    """ Ответ на запрос тарифов """
    totalCount: Optional[int] = 0
    payload: Optional[List[TariffItem]] = None
