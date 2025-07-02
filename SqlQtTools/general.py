import sys
from datetime import timezone, timedelta

from PySide6.QtWidgets import QApplication, QStyleFactory

tz_moscow = timezone(offset=timedelta(hours=3), name='Europe/Moscow')


def pyside6_show(main_window, style="Fusion"):
    try:
        import ctypes

        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    finally:
        qtapp = QApplication(sys.argv)
        qtapp.setStyle(QStyleFactory.create(style))
        main_window()
        main_window.show()
        qtapp.exec()