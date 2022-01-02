import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication

from MyEnums import Names
from QMyClientList import QMyClientList
from QMyCreateClient import QMyCreateClient


def start_main_program():
    if __name__ == Names.MAIN_PYTHON_PROCESS.value:
        app = QApplication(sys.argv)
        stack_widget = QtWidgets.QStackedWidget()
        init_widgets(stack_widget)
        stack_widget.show()
        sys.exit(app.exec())

def init_widgets(stack_widget):
    for WidgetClass in [QMyCreateClient, QMyClientList]:
        widget = WidgetClass()
        widget.setMinimumWidth(800)
        widget.setMinimumHeight(1000)
        stack_widget.addWidget(widget)

    return widget


start_main_program()
