from typing import TypeVar

from SqlQtTools.sql.model import SysBaseTable

SQLTableType = TypeVar("SQLTableType", bound=SysBaseTable)

from SqlQtTools.sql.dao import SysBaseDAO

SQLDAOType = TypeVar("SQLDAOType", bound=SysBaseDAO)

from SqlQtTools.sql.make import init_db, update_db
from SqlQtTools.sql.model import BaseTable, BaseExtTable
