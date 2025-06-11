from typing import TypeVar

from SqlQtTools.sql.make import init_db, update_db
from SqlQtTools.sql.model import SysBaseTable, BaseTable, BaseExtTable
from SqlQtTools.sql.dao import SysBaseDAO


SQLTableType = TypeVar("SQLTableType", bound=SysBaseTable)
SQLDAOType = TypeVar("SQLDAOType", bound=SysBaseDAO)