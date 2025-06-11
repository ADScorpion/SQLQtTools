from typing import TypeVar

from SqlQtTools.qt.model import SysBaseDS

DataSourceType = TypeVar("DataSourceType", bound=SysBaseDS)

from SqlQtTools.qt.icons import BootstrapIcons, icon_provider
from SqlQtTools.qt.dialogs import SysBaseDialog
from SqlQtTools.qt.forms import SysBaseMainWindow, SysBaseWidgetView
