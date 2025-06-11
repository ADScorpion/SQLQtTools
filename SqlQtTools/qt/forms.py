from PyQt6.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMdiArea, QMessageBox, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QHeaderView, QTableView, QStatusBar, QWidget


from SqlQtTools.qt.icons import icon_provider, BootstrapIcons
from SqlQtTools.qt.dialogs import SysBaseDialog
from SqlQtTools.qt import DataSourceType


class SysBaseMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self.init_menubar()

    def init_menubar(self):
        """Инициализация меню"""
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")
        for action in self.menu_file():
            file_menu.addAction(action)
        file_menu.addSeparator()
        exit_action = QAction(icon_provider.get_icon(BootstrapIcons.POWER), "Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.menu_add(menubar)

        # Меню "Окно"
        window_menu = menubar.addMenu("Окно")
        tile_action = QAction(icon_provider.get_icon(BootstrapIcons.WINDOW_SPLIT), "Мозаика", self)
        tile_action.setStatusTip("Окна перестраиваются в порядке мозайки")
        tile_action.setShortcut('F2')
        tile_action.triggered.connect(self.mdi.tileSubWindows)
        window_menu.addAction(tile_action)
        cascade_action = QAction(icon_provider.get_icon(BootstrapIcons.WINDOW_STACK), "Каскад", self)
        cascade_action.setShortcut('F3')
        cascade_action.triggered.connect(self.mdi.cascadeSubWindows)
        window_menu.addAction(cascade_action)
        close_action = QAction(icon_provider.get_icon(BootstrapIcons.WINDOW_X), "Закрыть", self)
        close_action.setShortcut('F4')
        close_action.triggered.connect(self.window_close_active)
        window_menu.addAction(close_action)

    def window_close_active(self):
        """Закрытие активного окна"""
        active_subwindow = self.mdi.activeSubWindow()
        if active_subwindow:
            widget = active_subwindow.widget()
            active_subwindow.close()

    def menu_file(self):
        return []

    def menu_add(self, menubar):
        pass


class SysBaseWidgetView(QWidget):
    model: type[DataSourceType]
    dialog = SysBaseDialog
    title = "Форма #"
    win_icon = BootstrapIcons.ROCKET_TAKEOFF
    action = None

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.proxy_model = QSortFilterProxyModel()
        self.status_bar = QStatusBar()
        self.view = QTableView()
        self.view.horizontalHeader().setStretchLastSection(True)
        self.datasource = None
        self.parent_id = None
        self.query = None
        self.setWindowTitle(self.title)

        data = kwargs.pop('data', None)
        where = kwargs.pop('where', None)
        self.init_model(parent, data, where)
        self.init_ui()

    def init_model(self, parent, data, where):
        if data:
            self.setWindowTitle(f"{str(data)} {self.title}")
            self.parent_id = data.Id

        if where:
            self.query = self.model.dao.query(*where)

    def init_ui(self):
        try:
            self.datasource = self.model(self.query)
            self.proxy_model.setSourceModel(self.datasource)
            self.proxy_model.setFilterKeyColumn(-1)

            self.view.setModel(self.proxy_model)
            self.view.setSortingEnabled(True)
            self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            self.view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

            btn_add = QPushButton("Добавить")
            btn_add.clicked.connect(self.add)
            btn_edit = QPushButton("Редактировать")
            btn_edit.clicked.connect(self.edit)
            btn_delete = QPushButton("Удалить")
            btn_delete.clicked.connect(self.delete)
            btn_close = QPushButton("Закрыть окно")
            btn_close.clicked.connect(self.close_window)

            search_layout = QHBoxLayout()
            icon = QLabel()
            icon.setPixmap(icon_provider.get_icon(BootstrapIcons.FUNNEL).pixmap(QSize(16, 16)))
            search_layout.addWidget(icon)
            search_edit = QLineEdit()
            search_edit.setPlaceholderText("Поиск...")
            search_edit.textChanged.connect(self.filter_data)
            search_layout.addWidget(search_edit)

            button_layout = QVBoxLayout()
            button_layout.addWidget(btn_add)
            button_layout.addWidget(btn_edit)
            button_layout.addWidget(btn_delete)

            for btn in self.add_button():
                button_layout.addWidget(btn)
            button_layout.addStretch()
            button_layout.addWidget(btn_close)

            self.status_bar.setSizeGripEnabled(False)

            grid_layout = QHBoxLayout()
            grid_layout.addWidget(self.view)
            grid_layout.addLayout(button_layout)

            main_layout = QVBoxLayout()
            main_layout.addLayout(search_layout)
            main_layout.addLayout(grid_layout)
            main_layout.addWidget(self.status_bar)

            self.setLayout(main_layout)

            self.update_status()
        except Exception as e:
            print(e)

    def add_button(self) -> list[QPushButton]:
        return []

    def update_status(self):
        """Обновление строки статуса с количеством записей"""
        try:
            row_count = self.datasource.rowCount()
            filtered_count = self.proxy_model.rowCount()

            if filtered_count == row_count:
                self.status_bar.showMessage(f"Всего записей: {row_count}")
            else:
                self.status_bar.showMessage(f"Показано: {filtered_count} из {row_count} записей")
        except Exception as e:
            print(e)

    def filter_data(self, text):
        """Фильтрация данных в таблице"""
        self.proxy_model.setFilterRegularExpression(text)
        self.update_status()

    def add(self):
        """Добавление новой записи"""
        try:
            dialog = self.dialog(parent=self, data=self.datasource.model(), title=f"Добавление", query=self._add_dialog_filter())
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data(dao=self.datasource.dao)
                if data:
                    self._add_data(data)
                    self.datasource.reread()
                    self.view.scrollToBottom()
        except Exception as e:
            print(e)
        finally:
            self.update_status()

    def _add_data(self, data):
        return self.datasource.add(data)

    def _add_dialog_filter(self):
        return {}

    def edit(self):
        """Редактирование выбранной записи"""
        try:
            selected = self.view.selectionModel().selectedRows()
            if not selected:
                QMessageBox.warning(self, "Ошибка", "Выберите строку для редактирования")
                return

            source_index = self.proxy_model.mapToSource(selected[0])
            row = source_index.row()
            data = self.datasource.rows[row]

            dialog = self.dialog(parent=self, data=data, title=f"Редактирование")
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data_new = dialog.get_data(dao=self.datasource.dao)
                if data_new:
                    self._edit_data(row, data_new)
                    self.datasource.reread()
        except Exception as e:
            print(e)
        finally:
            self.update_status()

    def _edit_data(self, row, data):
        self.datasource.update(row, data)

    def delete(self):
        """Удаление выбранной записи"""
        try:
            selected = self.view.selectionModel().selectedRows()
            if not selected:
                QMessageBox.warning(self, "Ошибка", "Выберите строку для удаления")
                return

            source_indexes = [self.proxy_model.mapToSource(index) for index in selected]

            reply = QMessageBox.question(
                self, 'Подтверждение',
                'Вы уверены, что хотите удалить выбранную строку?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                for index in sorted(source_indexes, reverse=True):
                    self._delete_data(index.row())
                self.datasource.reread()
        except Exception as e:
            print(e)
        finally:
            self.update_status()

    def _delete_data(self, row_index):
        return self.datasource.remove(row_index)

    def close_window(self):
        """Закрытие текущего окна"""
        self.close()
        self.parent().close()

    def closeEvent(self, a0):
        super().closeEvent(a0)

    @classmethod
    def init_action(cls, parent=None):
        cls.action = QAction(icon_provider.get_icon(cls.win_icon), cls.title, parent)
        cls.action.triggered.connect(lambda: cls.active_triggered(parent, cls(parent=parent)))
        return cls.action

    def active_triggered(self, parent=None, children=None):
        subwindow = self.mdi.addSubWindow(parent)
        subwindow.setWindowIcon(icon_provider.get_icon(parent.win_icon))
        subwindow.show()

    @property
    def selected_data(self):
        selected = self.view.selectionModel().selectedRows()
        if not selected:
            return None
        source_index = self.proxy_model.mapToSource(selected[0])
        row = source_index.row()
        return self.datasource.rows[row]

    def keyPressEvent(self, event):
        match event.key():
            case Qt.Key.Key_F5:
                self.datasource.reread()
            case Qt.Key.Key_Escape:
                self.close_window()
            case _:
                super().keyPressEvent(event)

    @classmethod
    def init_view(cls, view, parent, data, field):
        if not data:
            return
        _view = view(parent=parent, data=data, where=[field == data.Id, ])
        subwindow = parent.window().mdi.addSubWindow(_view)
        subwindow.setWindowIcon(icon_provider.get_icon(_view.win_icon))
        subwindow.show()
        parent.window().update_status_bar()
