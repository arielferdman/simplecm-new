from QMyBaseWindow import QMyBaseWindow
from MyEnums import Layouts


class ClientList(QMyBaseWindow):
    def __init__(self, parent=None):
        super(ClientList, self).__init__()
        self.load_ui()

    def init_layout(self):
        self.layout = Layouts.CLIENT_LIST.value
