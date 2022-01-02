import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication

from MyEnums import Names
from QMyCreateClient import QMyCreateClient


def start_main_program(__name__, Main):
    if __name__ == Names.MAIN_PYTHON_PROCESS.value:
        app = QApplication(sys.argv)
        widget = QtWidgets.QStackedWidget()
        main = Main()
        main.setMinimumWidth(800)
        main.setMinimumHeight(1000)
        main.show()
        dir(main)
        sys.exit(app.exec())


start_main_program(__name__, QMyCreateClient)
