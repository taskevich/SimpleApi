from fastapi import APIRouter

from backend.backend.schemas import *
from backend.backend.models import DB

router = APIRouter()


@router.post("/api/admin/tariff", response_model=CreateTariffResponse, tags=["API", "ADMIN"])
async def add_ticket(request: CreateTariffRequest):
    error = await DB().create_tariff(request.tariffName, request.tariffDescription, request.tariffPrice)

    if error:
        return CreateTariffResponse(error=True, message="Ошибка создания тарифа")

    return CreateTariffResponse()


@router.delete("/api/admin/tariff", response_model=DeleteTariffResponse, tags=["API", "ADMIN"])
async def delete_tariff(request: DeleteTariffRequest):
    error = await DB().delete_tariff(request.tariffId)

    if error:
        return DeleteTariffResponse(error=True, message="Ошибка удаления тарифа")

    return DeleteTariffResponse()


@router.post("/api/admin/link-feature", response_model=LinkFeatureResponse, tags=["API", "ADMIN"])
async def link_feature(request: LinkFeatureRequest):
    error = await DB().link_feature(request.tariffId, request.payload.name, request.payload.max_services,
                                    request.payload.max_rows, request.payload.max_files)

    if error:
        return LinkFeatureResponse(error=True, message="Ошибка привязки фичи")

    return LinkFeatureResponse()


@router.delete("/api/admin/unlink-feature", response_model=UnLinkFeatureResponse, tags=["API", "ADMIN"])
async def unlink_feature(request: UnLinkFeatureRequest):
    error = await DB().unlink_feature(request.tariffId, request.featureId)

    if error:
        return UnLinkFeatureResponse(error=True, message="Ошибка отвязки фичи")

    return UnLinkFeatureResponse()


@router.post("/api/admin/link-discount", response_model=LinkDiscountResponse, tags=["API", "ADMIN"])
async def link_feature(request: LinkDiscountRequest):
    error = await DB().link_discount(request.tariffId, request.discount.name, request.discount.value)

    if error:
        return LinkFeatureResponse(error=True, message="Ошибка привязки фичи")

    return LinkFeatureResponse()


@router.post("/api/admin/unlink-discount", response_model=UnLinkDiscountResponse, tags=["API", "ADMIN"])
async def unlink_discount(request: UnLinkDiscountRequest):
    error = await DB().unlink_discount(request.tariffId, request.discountId)

    if error:
        return UnLinkDiscountResponse(error=True, message="Ошибка отвязки скидки")

    return UnLinkDiscountResponse()
