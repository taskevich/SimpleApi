from uuid import uuid4
from threading import Lock
from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey, text, DateTime, ForeignKeyConstraint, \
    Boolean, select, or_, func, insert, delete
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
    tariff_id = Column(Integer, ForeignKey("tariffs.id", ondelete="all, cascade"), nullable=False)


class Discounts(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
    value = Column(Float, server_default=text("0"))
    tariff_id = Column(Integer, ForeignKey("tariffs.id", ondelete="all, cascade"), nullable=False)


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
    tariff_features = relationship("Features", lazy="subquery")
    tariff_discount = relationship("Discounts", lazy="subquery")


class TariffExpire(Base):
    __tablename__ = "tariff_expire"

    id = Column(Integer, primary_key=True, nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"))
    start_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    end_date = Column(DateTime)


class UserHasTariff(Base):
    __tablename__ = "user_has_tariff"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="all, cascade"), nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id", ondelete="all, cascade"), nullable=False)


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
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
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

    async def get_tariffs(self) -> tuple[int, list[Tariffs]]:
        async with self.create_session() as session:
            session: AsyncSession
            tariffs = (await session.execute(select(Tariffs).order_by(Tariffs.id))).scalars().all()
            tariffs_count = (await session.execute(select(func.count(Tariffs.id)))).scalar()
            return tariffs_count, tariffs

    async def get_user_tariff(self, user_id: int):
        async with self.create_session() as session:
            session: AsyncSession
            try:
                tariff = (
                    await session.execute(
                        select(Tariffs).join(UserHasTariff, UserHasTariff.user_id == user_id)
                        .where(Tariffs.id == UserHasTariff.tariff_id)
                    )
                ).scalar_one_or_none()
                return tariff
            except Exception as ex:
                logger.error(f"Ошибка получения тарифа пользователя: {ex}")

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

    async def delete_tariff(self, tariff_id: int):
        async with self.create_session() as session:
            session: AsyncSession
            try:
                await session.execute(
                    delete(Tariffs)
                    .where(Tariffs.id == tariff_id)
                )
                await session.commit()
            except Exception as ex:
                await session.rollback()
                logger.error(f"Ошибка удаления тарифа: {ex}")
                return True

    async def link_feature(self, tariff_id: int, name: str, max_services: int, max_rows: int, max_files: int):
        async with self.create_session() as session:
            session: AsyncSession
            try:
                await session.execute(
                    insert(Features)
                    .values(
                        name=name,
                        max_services=max_services,
                        max_rows=max_rows,
                        max_files=max_files,
                        tariff_id=tariff_id
                    )
                )
                await session.commit()
                return False
            except Exception as ex:
                logger.error(f"Ошибка привязки фичи: {ex}")
                return True

    async def link_discount(self, tariff_id: int, name: str, value: float):
        async with self.create_session() as session:
            session: AsyncSession
            try:
                await session.execute(
                    insert(Discounts)
                    .values(
                        name=name,
                        value=value,
                        tariff_id=tariff_id
                    )
                )
                await session.commit()
                return False
            except Exception as ex:
                logger.error(f"Ошибка привязки скидки: {ex}")
                return True

    async def unlink_discount(self, tariff_id: int, discount_id: int):
        async with self.create_session() as session:
            session: AsyncSession
            try:
                await session.execute(
                    delete(Discounts)
                    .where(Discounts.tariff_id == tariff_id, Discounts.id == discount_id)
                )
                await session.commit()
                return False
            except Exception as ex:
                logger.error(f"Ошибка отвязки скидки: {ex}")
                return True

    async def unlink_feature(self, tariff_id: int, feature_id: int):
        async with self.create_session() as session:
            session: AsyncSession
            try:
                await session.execute(
                    delete(Features)
                    .where(Features.tariff_id == tariff_id, Features.id == feature_id)
                )
                await session.commit()
                return False
            except Exception as ex:
                logger.error(f"Ошибка отвязки фичи: {ex}")
                return True

    async def create_tariff(self, name: str, description: str, price: int):
        async with self.create_session() as session:
            session: AsyncSession
            try:
                await session.execute(
                    insert(Tariffs)
                    .values(
                        name=name,
                        description=description,
                        price=price
                    )
                )
                await session.commit()
                return False
            except Exception as ex:
                await session.rollback()
                logger.error(f"Ошибка создания тарица: {ex}")
                return True

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
