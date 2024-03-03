from typing import Optional, Any, List
from pydantic import BaseModel


class DefaultResponse(BaseModel):
    """ Стандартный ответ на запрос """
    error: Optional[bool] = False
    message: Optional[str] = "OK"
    payload: Optional[Any] = None


class AuthRequest(BaseModel):
    """ Запрос на авторизацию """
    usernameOrEmail: Optional[str]
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
    usernameOrEmail: Optional[str]
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


class ServiceStatisticItem(BaseModel):
    """ Элемент статистики """
    id: Optional[int]
    filesCount: Optional[int]
    rowsCount: Optional[int]


class ServiceStatistic(DefaultResponse):
    """ Ответ на получении статистики сервиса """
    totalCount: Optional[int] = 0
    payload: Optional[ServiceStatisticItem]


class ServiceItem(BaseModel):
    """ Элемент сервиса """

    id: Optional[int]
    serviceName: Optional[str]
    isActive: Optional[bool]
    databaseName: Optional[str]
    tableName: Optional[str]
    createdAt: Optional[str]
    updatedAt: Optional[str]


class ServicesResponse(DefaultResponse):
    """ Ответ на получении статистики сервиса """
    totalCount: Optional[int] = 0
    payload: Optional[ServiceItem]


class PanelResponse(DefaultResponse):
    totalCount: Optional[int] = 0
    payload: Optional[Any] = None
