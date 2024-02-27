from uuid import uuid4
from threading import Lock
from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey, text, DateTime, ForeignKeyConstraint, Boolean
from contextlib import asynccontextmanager
from asyncpg import Connection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


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


class Discounts(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
    value = Column(Float, server_default=text("0"))


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        ForeignKeyConstraint(["role_id"], ["roles.id"], name="user_role_id_fk"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    phone = Column(String(16), nullable=True, unique=True)
    is_active = Column(Boolean)
    is_blocked = Column(Boolean, server_default=text("true"))
    role_id = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"),
                        onupdate=text("CURRENT_TIMESTAMP"))


class Tariffs(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, server_default=text("0"))


class TariffHasFeatures(Base):
    __tablename__ = "tariff_has_features"
    __table_args__ = (
        ForeignKeyConstraint(["tariff_id"], ["tariffs.id"], name="tariff_id_fk"),
        ForeignKeyConstraint(["feature_id"], ["features.id"], name="features_id_fk")
    )

    id = Column(Integer, primary_key=True, nullable=False)
    tariff_id = Column(Integer)
    feature_id = Column(Integer)


class TariffHasDiscount(Base):
    __tablename__ = "tariff_has_discount"
    __table_args__ = (
        ForeignKeyConstraint(["tariff_id"], ["tariffs.id"], name="tariff_id_fk"),
        ForeignKeyConstraint(["discount_id"], ["discounts.id"], name="discounts_id_fk")
    )

    id = Column(Integer, primary_key=True, nullable=False)
    tariff_id = Column(Integer)
    discount_id = Column(Integer)


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


#
#   Таблицы пользовательских сервисов
#

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
            await conn.run_sync(Base.metadata.create_all)

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
