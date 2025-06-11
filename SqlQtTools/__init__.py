DB_VERSION = 1
DB_FILE = 'config.db'

from SqlQtTools.general import tz_moscow, SQLTableType, SQLDAOType, DataSourceType
from SqlQtTools.sql.make import init_db, update_db
from SqlQtTools.sql.model import SysBaseTable, BaseTable, BaseExtTable
from SqlQtTools.sql.dao import SysBaseDAO
from SqlQtTools.qt.icons import BootstrapIcons, icon_provider
from SqlQtTools.qt.model import SysBaseDS
from SqlQtTools.qt.dialogs import SysBaseDialog
from SqlQtTools.qt.forms import SysBaseMainWindow, SysBaseWidgetView
