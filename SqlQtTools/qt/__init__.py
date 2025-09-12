from typing import TypeVar

from SqlQtTools.qt.model import SysBaseDS

DataSourceMap = TypeVar("DataSourceMap", bound=SysBaseDS)

from SqlQtTools.qt.icons import ResourceManager
from SqlQtTools.qt.dialogs import SysBaseDialog
from SqlQtTools.qt.forms import SysBaseMainWindow, SysBaseWidgetView, PySideApp
from SqlQtTools.qt.worker import ThreadManager, BaseTask, Worker
