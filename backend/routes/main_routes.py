import io

from PIL import Image
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from backend.backend.schemas import *
from backend.backend.config import *
from backend.backend.models import DB

router = APIRouter()


@router.get("/api/tariffs", response_model=TariffsResponse, tags=["API"])
async def tariffs():
    """ Маршрут получения тарифов """
    tariffs_count, tariffs = await DB().get_tariffs()

    response = TariffsResponse(
        totalCount=tariffs_count,
        payload=[
            TariffItem(
                name=tariff.name,
                description=tariff.description,
                discounts=DiscountResponse(
                    payload=[
                        DiscountItem(
                            id=discount.id,
                            name=discount.name,
                            value=discount.value
                        )
                        for discount in tariff.tariff_discount
                    ]
                ) if tariff.tariff_discount else None,
                features=FeaturesResponse(
                    payload=[
                        FeatureItem(
                            id=feature.id,
                            name=feature.name,
                            max_services=feature.max_services,
                            max_rows=feature.max_rows,
                            max_files=feature.max_files
                        ) for feature in tariff.tariff_features
                    ]
                ) if tariff.tariff_features else None,
                price=tariff.price,
                startDate=str(tariff.tariff_expire[0].start_date) if tariff.tariff_expire else None,
                endDate=str(tariff.tariff_expire[0].end_date) if tariff.tariff_expire else None
            )
            for tariff in tariffs
        ]
    )

    return response


@router.get("/api/resources/{name}", tags=["API"])
async def resources(name: str):
    """ Получение ресурса по имени """
    for resource in os.listdir(RESOURCES_PATH):
        if name.split(".")[0] == resource.split(".")[0]:
            image = Image.open(RESOURCES_PATH + f"/{resource}").convert("RGB")
            img_byte_array = io.BytesIO()
            image.save(img_byte_array, format="JPEG")
            img_byte_array.seek(0)
            return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/jpeg")
    return DefaultResponse(error=True, message="Изображение не найдено")
