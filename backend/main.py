from fastapi import FastAPI
from routes import main_routes, admin_routes, credentials_routes
from backend.backend.models import *
from backend.backend.logger import *

app = FastAPI()

app.include_router(main_routes.router)
app.include_router(admin_routes.router)
app.include_router(credentials_routes.router)


@app.on_event("startup")
async def on_startup():
    try:
        logger.info("Инициализация базы данных")
        await DB().initialize_connection()
        logger.info("База данных инициализирована")
    except Exception as ex:
        logger.error(f"Ошибка инициализации данных: {ex}")
