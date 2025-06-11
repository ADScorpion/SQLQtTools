from typing import TypeVar

from SqlQtTools.qt.icons import BootstrapIcons, icon_provider
from SqlQtTools.qt.model import SysBaseDS
from SqlQtTools.qt.dialogs import SysBaseDialog
from SqlQtTools.qt.forms import SysBaseMainWindow, SysBaseWidgetView

DataSourceType = TypeVar("DataSourceType", bound=SysBaseDS)