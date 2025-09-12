import sys

PYTHON_VERSION = sys.version_info

if PYTHON_VERSION >= (3, 10):
    try:
        from PySide6 import QtCore, QtGui, QtWidgets
        from PySide6.QtCore import Signal, Slot, QThread, QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel, QSize, QObject, QByteArray, QFile
        from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtWidgets import (QMainWindow, QMdiArea, QMessageBox, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QHeaderView, QTableView, QStatusBar,
                                       QWidget, QApplication, QStyleFactory, QFormLayout, QComboBox, QDateTimeEdit, QCheckBox, QDialogButtonBox, QTextEdit)

        PYSIDE_VERSION = 6
        HAS_MATCH_CASE = True
    except ImportError:
        from PySide2 import QtCore, QtGui, QtWidgets
        from PySide2.QtCore import Signal, Slot, QThread, QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel, QSize, QObject, QByteArray, QFile
        from PySide2.QtGui import QIcon, QPixmap, QPainter
        from PySide2.QtSvg import QSvgRenderer
        from PySide2.QtWidgets import (QAction, QMainWindow, QMdiArea, QMessageBox, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QHeaderView, QTableView,
                                       QStatusBar, QWidget, QApplication, QStyleFactory, QFormLayout, QComboBox, QDateTimeEdit, QCheckBox, QDialogButtonBox, QTextEdit)

        PYSIDE_VERSION = 5
        HAS_MATCH_CASE = True
else:
    from PySide2 import QtCore, QtGui, QtWidgets
    from PySide2.QtCore import Signal, Slot, QThread, QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel, QSize, QObject, QByteArray, QFile
    from PySide2.QtGui import QIcon, QPixmap, QPainter
    from PySide2.QtSvg import QSvgRenderer
    from PySide2.QtWidgets import (QAction, QMainWindow, QMdiArea, QMessageBox, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QHeaderView, QTableView,
                                   QStatusBar, QWidget, QApplication, QStyleFactory, QFormLayout, QComboBox, QDateTimeEdit, QCheckBox, QDialogButtonBox, QTextEdit)

    PYSIDE_VERSION = 5
    HAS_MATCH_CASE = False
