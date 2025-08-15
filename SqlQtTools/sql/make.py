import os

from sqlalchemy import text

from SqlQtTools import DB_FILE
from SqlQtTools.sql.model import engine, SysBaseTable


class SQLiteSynchronized:
    VERSION = 0

    def sync_db(self):
        import asyncio
        if not os.path.exists(DB_FILE):
            asyncio.run(self.__init_db())
        else:
            asyncio.run(self.__check_version())
            self.update_db()

    async def __init_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(SysBaseTable.metadata.create_all)

    async def __check_version(self):
        async with engine.begin() as conn:
            try:
                result = await conn.execute(text("PRAGMA user_version"))
                self.VERSION = result.scalar_one_or_none()[0]
            except:
                self.VERSION = 0

    async def __execute(self, sql_command):
        async with engine.begin() as conn:
            await conn.execute(text(sql_command))

    def update_db(self):
        import asyncio
        if self.VERSION < 1:
            asyncio.run(self.__execute(f"PRAGMA user_version = 1"))
