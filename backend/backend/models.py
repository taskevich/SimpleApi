from uuid import uuid4
from threading import Lock
from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey, text, DateTime, ForeignKeyConstraint, \
    Boolean, select, or_
from contextlib import asynccontextmanager
from asyncpg import Connection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, relationship

from backend.backend.logger import logger


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid4()}__'


class Base(DeclarativeBase):
    pass


#
#   Базовые таблицы
#

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    text_name = Column(String(32), nullable=False)


class Features(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
    max_services = Column(Integer, server_default=text("1"))
    max_rows = Column(Integer, server_default=text("5000"))
    max_files = Column(Integer, server_default=text("50"))


class Discounts(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
    value = Column(Float, server_default=text("0"))


class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    phone = Column(String(16), nullable=True, unique=True)
    is_active = Column(Boolean)
    is_blocked = Column(Boolean, server_default=text("TRUE"))
    is_receive_notifications = Column(Boolean, server_default=text("TRUE"))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"),
                        onupdate=text("CURRENT_TIMESTAMP"))

    role = relationship("Roles", lazy="subquery")


class Tariffs(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, server_default=text("0"))

    tariff_expire = relationship("TariffExpire", lazy="subquery")
    tariff_has_features = relationship("TariffHasFeatures", lazy="subquery")
    Tariff_has_discount = relationship("TariffHasDiscount", lazy="subquery")


class TariffExpire(Base):
    __tablename__ = "tariff_expire"

    id = Column(Integer, primary_key=True, nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"))
    start_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    end_date = Column(DateTime)


class TariffHasFeatures(Base):
    __tablename__ = "tariff_has_features"

    id = Column(Integer, primary_key=True, nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"), nullable=False)
    feature_id = Column(Integer, ForeignKey("features.id"), nullable=False)


class TariffHasDiscount(Base):
    __tablename__ = "tariff_has_discount"

    id = Column(Integer, primary_key=True, nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"), nullable=False)
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=False)


#
#   Таблицы пользовательских сервисов
#

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, nullable=False)
    service_name = Column(String(64), nullable=False)
    is_active = Column(Boolean, server_default=text("TRUE"))
    database_name = Column(String(32), nullable=False)
    table_name = Column(String(32), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"),
                        onupdate=text("CURRENT_TIMESTAMP"))


class UserHasService(Base):
    __tablename__ = "user_has_service"

    id = Column(Integer, primary_key=True, nullable=False)
    service_id = Column(Integer, ForeignKey("services"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class ServiceStatistic(Base):
    __tablename__ = "service_statistic"

    id = Column(Integer, primary_key=True, nullable=False)
    files_count = Column(Integer, server_default=text("0"))
    rows_count = Column(Integer, server_default=text("0"))


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DB(metaclass=SingletonMeta):
    def __init__(self):
        self.engine = create_async_engine(
            "postgresql+asyncpg://postgres:postgres@base:5432/simpleapi",
            echo=False, pool_pre_ping=True,
            future=True, connect_args={
                # "statement_cache_size": 0,
                # "prepared_statement_cache_size": 0,
                "connection_class": CConnection},
            # poolclass=NullPool
        )

        self.session = async_sessionmaker(self.engine,
                                          expire_on_commit=False,
                                          class_=AsyncSession)

    async def initialize_connection(self):
        async with self.engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def get_user_by_username_or_email(self, username: str) -> Users | None:
        async with self.create_session() as session:
            try:
                return (await session.execute(select(Users)
                                              .where(or_(Users.username == username,
                                                         Users.email == username)))).scalars().first()
            except Exception as ex:
                logger.error(f"Ошибка получения пользователя: {ex}")

    async def create_new_user(self, username: str, password: str, email: str,
                              phone: str | None = None, receive_notifications_email: bool = False):
        async with self.create_session() as session:
            try:
                if await self.get_user_by_username_or_email(username):
                    return True, "Пользователь уже существует"

                user = Users(
                    username=username,
                    password=password,
                    email=email,
                    phone=phone,
                    role_id=2,
                    is_receive_notifications=receive_notifications_email
                )

                session.add(user)
                await session.commit()
                return user, "Вы успешно зарегистрированы"
            except Exception as ex:
                logger.error(f"Ошибка создания пользователя: {ex}")
                return True, "Ошибка создания пользователя"

    async def create_role(self, name: str, text_name: str) -> Roles | None:
        async with self.create_session() as session:
            try:
                role = Roles(name=name, text_name=text_name)
                session.add(role)
                await session.commit()
                return role
            except Exception as ex:
                logger.error(f"Ошибка создания роли: {ex}")

    async def get_role_by_name(self, name: str) -> Roles | None:
        async with self.create_session() as session:
            try:
                return (await session.execute(select(Roles).where(Roles.name == name))).scalars().first()
            except Exception as ex:
                logger.error(f"Ошибка получения роли: {ex}")

    async def change_user_data(self, username_or_email: str, new_password: str = None,
                               new_email: str = None, new_phone: str = None, receive_email_notifications: bool = False):
        async with self.create_session() as session:
            try:
                user = await self.get_user_by_username_or_email(username_or_email)
                if not user:
                    return True, "Пользователь не найден"

                if new_password:
                    user.password = new_password
                if username_or_email:
                    user.username = username_or_email
                if new_email:
                    user.email = new_email
                if new_phone:
                    user.phone = new_phone
                if receive_email_notifications:
                    user.is_receive_notifications = receive_email_notifications

                await session.commit()
                return True, "Данные изменены"
            except Exception as ex:
                logger.error(f"Ошибка обновления данных пользователя: {ex}")

    @asynccontextmanager
    async def create_session(self):
        async with self.session() as db:
            try:
                yield db
            except Exception as e:
                await db.rollback()
                raise
            finally:
                await db.close()
