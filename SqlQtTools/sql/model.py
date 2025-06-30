from os import getlogin
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.ext.declarative import AbstractConcreteBase

from SqlQtTools import DB_FILE

database_url = f'sqlite+aiosqlite:///{DB_FILE}'
engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class SysBaseTable(AsyncAttrs, so.DeclarativeBase):
    """Базовое описание таблицы без базовых полей"""

    @classmethod
    def grid_overview(cls):
        return []


class SysBaseTableI(AbstractConcreteBase, SysBaseTable):
    """Базовое описание таблицы с полями Id"""

    Id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True, autoincrement=True, doc="Номер записи", info={'visible': False})


class SysBaseTableIC(AbstractConcreteBase, SysBaseTable):
    """Базовое описание таблицы с полями Id, CreatedBy, CreatedAt"""

    Id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True, autoincrement=True, doc="Номер записи", info={'visible': False})
    CreatedBy: so.Mapped[str] = so.mapped_column(String(100), default=getlogin(), doc="Создал", info={'visible': False})
    CreatedAt: so.Mapped[datetime] = so.mapped_column(default=sa.func.now(), doc="Создано", info={'visible': False})


class SysBaseTableICM(AbstractConcreteBase, SysBaseTable):
    """Базовое описание таблицы с полями Id, CreatedBy, CreatedAt, ModifiedBy, ModifiedAt"""

    Id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True, autoincrement=True, doc="Номер записи", info={'visible': False})
    CreatedBy: so.Mapped[str] = so.mapped_column(String(100), default=getlogin(), doc="Создал", info={'visible': False})
    CreatedAt: so.Mapped[datetime] = so.mapped_column(default=sa.func.now(), doc="Создано", info={'visible': False})
    ModifiedBy: so.Mapped[str | None] = so.mapped_column(String(100), onupdate=getlogin(), doc="Изменил", info={'visible': False})
    ModifiedAt: so.Mapped[datetime | None] = so.mapped_column(onupdate=sa.func.now(), doc="Изменено", info={'visible': False})
