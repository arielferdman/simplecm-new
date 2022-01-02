from MyEnums import Layouts
from QMyBaseWindow import QMyBaseWindow


class QMyClientList(QMyBaseWindow):
    def __init__(self, parent=None):
        super(QMyClientList, self).__init__()
        self.load_ui()

    def init_layout(self):
        self.layout = Layouts.CLIENT_LIST.value
