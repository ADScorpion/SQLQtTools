DB_VERSION = 1
DB_FILE = 'config.db'

from SqlQtTools.general import tz_moscow, SQLTableType, SQLDAOType, DataSourceType
from SqlQtTools.sql import init_db, update_db, SysBaseTable, BaseTable, BaseExtTable, SysBaseDAO
from SqlQtTools.qt import BootstrapIcons, icon_provider, SysBaseDS, SysBaseDialog, SysBaseMainWindow, SysBaseWidgetView
