from datetime import timezone, timedelta
from typing import TypeVar

from SqlQtTools.sql import SysBaseTable, SysBaseDAO
from SqlQtTools.qt import SysBaseDS

tz_moscow = timezone(offset=timedelta(hours=3), name='Europe/Moscow')

SQLTableType = TypeVar("SQLTableType", bound=SysBaseTable)
SQLDAOType = TypeVar("SQLDAOType", bound=SysBaseDAO)
DataSourceType = TypeVar("DataSourceType", bound=SysBaseDS)
