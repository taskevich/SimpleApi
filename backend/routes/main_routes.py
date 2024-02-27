import io
import os

from PIL import Image
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from backend.backend.schemas import *
from backend.backend.config import *

router = APIRouter()


@router.get("/api/tariffs", response_model=TariffsResponse, tags=["API"])
async def tariffs():
    """ Маршрут получения тарифов """
    return TariffsResponse()


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
