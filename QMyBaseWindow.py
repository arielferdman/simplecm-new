import json
import os
import sqlite3

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QWidget

from MyEnums import DataFileNames, FileOperations, Names


class QMyBaseWindow(QWidget):
    def __init__(self, parent=None):
        super(QMyBaseWindow, self).__init__()
        self.init_properties()
        self.load_ui()

    def init_properties(self):
        self.init_filesystem_props()
        self.init_qt_props()
        self.init_business_logic_props()

    def init_business_logic_props(self):
        self.set_up_db()
        self.init_column_names()

    def init_qt_props(self):
        self.init_layout()
        self.init_ui_loader()

    def init_layout(self):
        self.layout = None

    def init_filesystem_props(self):
        self.init_base_path()
        self.init_data_files_paths()

    def init_data_files_paths(self):
        self.init_column_names_file_path()
        self.init_create_db_query_file_path()

    def init_create_db_query_file_path(self):
        self.create_db_query_file_path = os.path.join(
            self.base_path, DataFileNames.CREATE_DB_QUERY.value)

    def init_column_names_file_path(self):
        self.column_names_file_path = os.path.join(
            self.base_path, DataFileNames.COLUMN_NAMES.value)

    def init_ui_loader(self):
        self.loader = QUiLoader()

    def init_base_path(self):
        self.base_path = os.getcwd()

    def init_column_names(self):
        self.columns = self.load_json(self.column_names_file_path)

    def load_json(self, filename):
        data = None
        with open(filename, FileOperations.READ.value) as in_file:
            data = json.loads(in_file.read())
        return data

    def load_ui(self):
        self.get_screen_file_path(self.layout)
        self.load_screen_ui_file()
        self.close_screen_ui_file()

    def load_screen(self, layout):
        self.get_screen_file_path(layout)
        self.load_screen_ui_file()
        self.close_screen_ui_file()

    def close_screen_ui_file(self):
        self.ui_file.close()

    def load_screen_ui_file(self):
        self.ui_file = QFile(self.path)
        self.ui_file.open(QFile.ReadOnly)
        self.ui = self.loader.load(self.ui_file, self)

    def get_screen_file_path(self, layout):
        self.get_root_dir_file_path(layout)

    def get_root_dir_file_path(self, filename):
        self.path = os.path.join(self.base_path, filename)

    def get_filename(self, file_path):
        return os.path.split(file_path)[1]

    def set_up_db(self):
        self.get_sqlite_connection()
        self.create_table_if_doesnt_exist()

    def close_sqlite_connection(self):
        self.con.close()

    def create_table_if_doesnt_exist(self):
        query = self.load_json(self.create_db_query_file_path)
        self.cur.execute(query)
        self.con.commit()

    def get_sqlite_connection(self):
        self.con = sqlite3.connect(Names.DB_NAME.value)
        self.cur = self.con.cursor()
