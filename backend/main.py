from fastapi import FastAPI
from routes import main_routes
from backend.backend.models import *
from backend.backend.logger import *

app = FastAPI()

app.include_router(main_routes.router)


@app.on_event("startup")
async def on_startup():
    try:
        logger.info("Инициализация базы данных")
        await DB().initialize_connection()
        logger.info("База данных инициализирована")
    except Exception as ex:
        logger.error(f"Ошибка инициализации данных: {ex}")
