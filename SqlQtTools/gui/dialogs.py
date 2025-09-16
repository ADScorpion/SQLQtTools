from datetime import UTC, datetime
from typing import Generic
from sqlalchemy import Float, Integer, Enum, DateTime, Boolean, String

from SqlQtTools.qt.core import QDialog, QFormLayout, QLineEdit, QComboBox, QDateTimeEdit, QCheckBox, QDialogButtonBox, QTextEdit
from SqlQtTools.general import tz_moscow
from SqlQtTools.sql.dao import SysBaseDAO
from SqlQtTools.gui import DataSourceMap


class SysBaseDialog(QDialog, Generic[DataSourceMap]):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        title = kwargs.pop('title', "Dialog")
        self.setWindowTitle(title)
        self.columns = dict()
        self._datasource = kwargs.pop('data')
        self.query = kwargs.pop('query', [])
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        model = self._datasource
        for column in model.__table__.columns:
            if column.info and 'visible' in column.info and column.info['visible'] is False:
                continue
            value = getattr(model, column.name)
            if isinstance(column.type, Float):
                self.columns[column.name] = QLineEdit(f"{value:.2f}")
                layout.addRow(f"{column.doc}:", self.columns[column.name])
            elif isinstance(column.type, Integer):
                if column.foreign_keys:
                    for fk in column.foreign_keys:
                        obj_combobox = QComboBox()
                        i = 0
                        current_index = 0
                        for element in self._get_elements(fk.column.table.name):
                            obj_combobox.addItem(element.Name, element.Id)
                            if element.Id == value:
                                current_index = i
                            i += 1
                        if value:
                            obj_combobox.setCurrentIndex(current_index)
                    self.columns[column.name] = obj_combobox
                    layout.addRow(f"{column.doc}:", self.columns[column.name])
                else:
                    self.columns[column.name] = QLineEdit(f"{value}")
                    layout.addRow(f"{column.doc}:", self.columns[column.name])
            elif isinstance(column.type, Enum):
                obj_combobox = QComboBox()
                for element in column.type.enum_class:
                    obj_combobox.addItem(element.value, element.name)
                if value:
                    obj_combobox.setCurrentText(value.value)
                self.columns[column.name] = obj_combobox
                layout.addRow(f"{column.doc}:", self.columns[column.name])
            elif isinstance(column.type, DateTime):
                obj_datetime = QDateTimeEdit()
                obj_datetime.setDisplayFormat("dd.MM.yyyy HH:mm")
                if value is not None:
                    utc_dt = value.replace(tzinfo=UTC)
                    local_dt = utc_dt.astimezone(tz=tz_moscow)
                    obj_datetime.setDateTime(local_dt)
                self.columns[column.name] = obj_datetime
                layout.addRow(f"{column.doc}:", self.columns[column.name])
            elif isinstance(column.type, Boolean):
                obj_checkbox = QCheckBox()
                obj_checkbox.setChecked(value)
                self.columns[column.name] = obj_checkbox
                layout.addRow(f"{column.doc}:", self.columns[column.name])
            elif isinstance(column.type, String):
                self.columns[column.name] = QLineEdit(value)
                layout.addRow(f"{column.doc}:", self.columns[column.name])
            else:
                raise NotImplementedError()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

        self.setLayout(layout)

    def get_data(self, dao):
        for column in self._datasource.__table__.columns:
            if column.name in self.columns:
                q_object = self.columns[column.name]
                if isinstance(q_object, QLineEdit):
                    if isinstance(getattr(self._datasource, column.name), int):
                        setattr(self._datasource, column.name, int(q_object.text()))
                    else:
                        setattr(self._datasource, column.name, q_object.text())
                elif isinstance(q_object, QComboBox):
                    setattr(self._datasource, column.name, q_object.currentData())
                elif isinstance(q_object, QCheckBox):
                    setattr(self._datasource, column.name, q_object.isChecked())
                elif isinstance(q_object, QDateTimeEdit):
                    setattr(self._datasource, column.name, datetime.strptime(q_object.text(), "%d.%m.%Y %H:%M").astimezone(tz=UTC))
                elif isinstance(q_object, QTextEdit):
                    setattr(self._datasource, column.name, q_object.toPlainText())
        return self._datasource

    def _get_elements(self, table_name):
        dao = SysBaseDAO.construct(table_name)
        query = self.query[table_name] if table_name in self.query else None
        return dao.select(query)
