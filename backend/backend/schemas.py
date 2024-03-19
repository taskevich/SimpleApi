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


class RegistrationResponse(DefaultResponse):
    """ Ответ на запрос регистрации """


class DeleteTariffRequest(BaseModel):
    """ Запрос на удаление тарифа """
    tariffId: Optional[int]


class DeleteTariffResponse(DefaultResponse):
    """ Ответ на удаление тарифа """


class CreateTariffRequest(BaseModel):
    """ Запрос на создание тарифа """
    tariffName: Optional[str]
    tariffDescription: Optional[str]
    tariffPrice: Optional[int]


class CreateTariffResponse(DefaultResponse):
    """ Ответ на создание тарифа """


class RecoveryRequest(DefaultResponse):
    """ Запрос на восстановление аккаунта """
    usernameOrEmail: Optional[str]
    newPassword: Optional[str]


class RecoveryResponse(DefaultResponse):
    """ Ответ на восстановление аккаунта """


class FeatureItem(BaseModel):
    """ Элемент фичи """
    id: Optional[int]
    name: Optional[str]
    max_services: Optional[int]
    max_rows: Optional[int]
    max_files: Optional[int]


class FeatureSecondItem(BaseModel):
    """ Элемент фичи """
    name: Optional[str]
    max_services: Optional[int]
    max_rows: Optional[int]
    max_files: Optional[int]


class LinkFeatureRequest(BaseModel):
    """ Запрос на привязку фичи """
    tariffId: Optional[int]
    payload: Optional[FeatureSecondItem]


class LinkFeatureResponse(DefaultResponse):
    """ Ответ на привязку фичи """


class UnLinkFeatureRequest(BaseModel):
    """ Запрос на отвязку фичи """
    tariffId: Optional[int]
    featureId: Optional[int]


class UnLinkFeatureResponse(DefaultResponse):
    """ Ответ на отвязку фичи """


class FeaturesResponse(DefaultResponse):
    """ Ответ на получение фич """
    payload: Optional[List[FeatureItem]] = None


class DiscountItem(BaseModel):
    """ Элемент скидки """
    id: Optional[int]
    name: Optional[str]
    value: Optional[float]


class DiscountSecondItem(BaseModel):
    """ Элемент скидки """
    name: Optional[str]
    value: Optional[float]


class LinkDiscountRequest(BaseModel):
    """ Запрос на привязку скидки """
    tariffId: Optional[int]
    discount: Optional[DiscountSecondItem]


class LinkDiscountResponse(DefaultResponse):
    """ Ответ на отвязку скидки """


class UnLinkDiscountRequest(BaseModel):
    """ Запрос на отвязку скидвки """
    tariffId: Optional[int]
    discountId: Optional[int]


class UnLinkDiscountResponse(DefaultResponse):
    """ Ответ на отвязку скидки """


class DiscountResponse(DefaultResponse):
    payload: Optional[List[DiscountItem]] = None


class TariffItem(BaseModel):
    """ Элемент тарифа """
    name: Optional[str]
    description: Optional[str]
    discounts: Optional[DiscountResponse] = None
    price: Optional[int] = None
    features: Optional[FeaturesResponse] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


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
