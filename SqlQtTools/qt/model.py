from datetime import timezone, datetime
from typing import Generic

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from sqlalchemy import Enum, DateTime

from SqlQtTools.sql import SQLDAOType
from SqlQtTools.general import tz_moscow


class SysBaseDS(QAbstractTableModel, Generic[SQLDAOType]):
    dao: type[SQLDAOType]

    def __init__(self, query=None, **kwargs):
        super().__init__()
        self._query = query
        env = kwargs.pop('env', None)
        self.dao.environment(env)
        self._db = self.dao.select(self._query)
        self._header = self.dao.header_by_fields(self.dao.model.grid_overview())

    def rowCount(self, parent=QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = self._db[index.row()]

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            field = self.dao.model.grid_overview()[index.column()]
            if field.info and 'data' in field.info:
                return getattr(row, field.info['data'])
            if isinstance(field.type, Enum):
                return getattr(row, field.name).value
            if isinstance(field.type, DateTime):
                if getattr(row, field.name):
                    utc_dt = getattr(row, field.name)
                    utc_dt = utc_dt.replace(tzinfo=timezone.utc)
                    local_dt = utc_dt.astimezone(tz=tz_moscow)
                else:
                    local_dt = datetime.min
                return local_dt.strftime("%d.%m.%Y %H:%M:%S")
            return getattr(row, field.name)

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self._header[section]
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return super().flags(index) | ~Qt.ItemFlag.ItemIsEditable

    @property
    def rows(self):
        return self._db

    def remove(self, row):
        data_id = None
        try:
            if 0 <= row <= self.rowCount():
                self.beginRemoveRows(QModelIndex(), row, row)
                data = self.rows.pop(row)
                self.dao.delete(data)
                self.endRemoveRows()
        except Exception as e:
            print(e)
        return data_id

    def add(self, row):
        try:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            row = self.dao.insert(row)
            self.endInsertRows()
        except Exception as e:
            print(e)
        return self.dao.get(row.Id)

    def update(self, row, data):
        try:
            self.dao.update(data)
            self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount() - 1))
        except Exception as e:
            print(e)

    def reread(self):
        self.layoutAboutToBeChanged.emit()
        self._db = self.dao.select(self._query)
        self.layoutChanged.emit()

    @property
    def model(self):
        return self.dao.model