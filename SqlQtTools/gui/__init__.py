from typing import TypeVar

from SqlQtTools.gui.model import SysBaseDS

DataSourceMap = TypeVar("DataSourceMap", bound=SysBaseDS)

from SqlQtTools.gui.icons import ResourceManager
from SqlQtTools.gui.dialogs import SysBaseDialog
from SqlQtTools.gui.forms import SysBaseMainWindow, SysBaseWidgetView, PySideApp
from SqlQtTools.gui.worker import ThreadManager, BaseTask, Worker