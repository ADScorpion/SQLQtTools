from typing import TypeVar

from SqlQtTools.sql.model import SysBaseTable

SQLTableMap = TypeVar("SQLTableMap", bound=SysBaseTable)

from SqlQtTools.sql.dao import SysBaseDAO

SQLDAOMap = TypeVar("SQLDAOMap", bound=SysBaseDAO)

from SqlQtTools.sql.make import SQLiteSynchronized
from SqlQtTools.sql.model import SysBaseTableI, SysBaseTableIC, SysBaseTableICM
