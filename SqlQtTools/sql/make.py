import os

from sqlalchemy import text

from SqlQtTools import DB_FILE
from SqlQtTools.sql.model import engine, SysBaseTable


async def __init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SysBaseTable.metadata.create_all)


async def __check_version():
    async with engine.begin() as conn:
        try:
            result = await conn.execute(text("PRAGMA user_version"))
            version = result.scalar_one_or_none()[0]
        except:
            version = 0
        return version


async def __execute(sql_command):
    async with engine.begin() as conn:
        await conn.execute(text(sql_command))


def update_db(version):
    import asyncio
    if version < 1:
        asyncio.run(__execute(f"PRAGMA user_version = 1"))
    if version < 2:
        pass


def init_db():
    import asyncio
    if not os.path.exists(DB_FILE):
        asyncio.run(__init_db())
    else:
        version = asyncio.run(__check_version())
        update_db(version)
