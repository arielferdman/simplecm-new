import os
import shutil
import sqlite3
import sys
import json
from enum import Enum
from pathlib import Path

from PySide6 import QtCore, QtGui
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow


class SqlParts(Enum):
    INSERT_START = 'insert into clients('
    INSERT_MID = ') values ('
    INSERT_END = ')'


class Names(Enum):
    COMMENTS_COLUMN_NAME = 'comments'
    DB_NAME = 'simplecm.db'
    MAIN_PYTHON_PROCESS = '__main__'


class StringParts(Enum):
    EMPTY_STRING = ''
    COMMA_SPACE = ', '
    QUESTION_MARK_COMMA_SPACE = '?, '


class FileOperations(Enum):
    READ = 'r'


class DirNames(Enum):
    CLIENT_DOCUMENTS_DIR = 'files'


class DataFileNames(Enum):
    INITIAL_FORM_DATA = 'initial_form_data.json'
    CREATE_DB_QUERY = 'create_db_query.json'
    COLUMN_NAMES = 'column_names.json'
    DOCUMENT_ICON = 'file-line.svg'


class Layouts(Enum):
    CREATE_CLIENT = 'form.ui'
    CLIENT_LIST = 'client_list.ui'


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__()
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
        self.init_ui_loader()

    def init_filesystem_props(self):
        self.init_base_path()
        self.init_base_dir()
        self.init_documents_dir()
        self.init_new_filepaths_property()
        self.init_data_files_paths()

    def init_data_files_paths(self):
        self.init_column_names_file_path()
        self.init_create_db_query_file_path()
        self.init_initial_form_data_file_path()

    def init_initial_form_data_file_path(self):
        self.initial_form_data_file_path = os.path.join(
            self.base_dir, DataFileNames.INITIAL_FORM_DATA.value)

    def init_create_db_query_file_path(self):
        self.create_db_query_file_path = os.path.join(
            self.base_dir, DataFileNames.CREATE_DB_QUERY.value)

    def init_column_names_file_path(self):
        self.column_names_file_path = os.path.join(
            self.base_dir, DataFileNames.COLUMN_NAMES.value)

    def init_ui_loader(self):
        self.loader = QUiLoader()

    def create_client_document_folder(self):
        self.create_client_documents_folder_name()
        self.create_client_document_folder_path()
        if not os.path.exists(self.client_documents_folder_path):
            os.mkdir(self.client_documents_folder_path)

    def create_client_document_folder_path(self):
        self.client_documents_folder_path = os.path.join(
            self.base_dir, self.documents_dir, self.client_documents_folder_name)

    def create_client_documents_folder_name(self):
        self.client_documents_folder_name = \
            f'{self.form_data[0]}-{self.form_data[1]}-{self.form_data[2]}'

    def init_new_filepaths_property(self):
        self.full_moved_file_paths = []

    def init_documents_dir(self):
        self.documents_dir = DirNames.CLIENT_DOCUMENTS_DIR.value

    def init_base_dir(self):
        self.base_dir = os.getcwd()

    def init_column_names(self):
        self.columns = self.load_json(self.column_names_file_path)

    def load_json(self, filename):
        data = None
        with open(filename, FileOperations.READ.value) as in_file:
            data = json.loads(in_file.read())
        return data

    def load_ui(self):
        self.get_screen_file_path(Layouts.CREATE_CLIENT)
        self.load_screen_ui_file()
        self.close_screen_ui_file()
        self.get_columns_properties()
        self.create_additional_widgets()
        self.fill_in_form()
        self.add_icon_to_button()

    def load_screen(self, layout):
        self.get_screen_file_path(layout)
        self.load_screen_ui_file()
        self.close_screen_ui_file()

    def get_columns_properties(self):
        for column_name in self.columns:
            setattr(self, column_name, getattr(self.ui, column_name))

    def close_screen_ui_file(self):
        self.ui_file.close()

    def create_additional_widgets(self):
        self.create_client_button = self.ui.create_client_button
        self.create_client_button.clicked.connect(self.create_client)
        self.documents_button = self.ui.documents_button
        self.documents_button.clicked.connect(self.select_documents)
        self.documents.hide()

    def load_screen_ui_file(self):
        self.ui_file = QFile(self.path)
        self.ui_file.open(QFile.ReadOnly)
        self.ui = self.loader.load(self.ui_file, self)

    def get_screen_file_path(self, layout):
        self.get_root_dir_file_path(layout)

    def get_root_dir_file_path(self, filename):
        self.path = os.path.join(self.base_path, filename.value)

    def init_base_path(self):
        self.base_path = os.fspath(Path(__file__).resolve().parent)

    def add_icon_to_button(self):
        self.documents_button.setIcon(QtGui.QIcon(DataFileNames.DOCUMENT_ICON.value))
        self.documents_button.setIconSize(QtCore.QSize(24, 24))

    def fill_in_form(self):
        initial_form_data = self.load_json(self.initial_form_data_file_path)
        for key, value in initial_form_data.items():
            getattr(self, key).setText(value)

    def select_documents(self):
        self.get_documents_paths()

    def get_documents_paths(self):
        self.documents_paths = QFileDialog.getOpenFileNames()[0]

    def update_documents(self):
        self.documents.setText(json.dumps(self.full_moved_file_paths))

    def get_documents_filenames(self):
        return [self.get_filename(file_path) for file_path in self.documents_paths]

    def get_filename(self, file_path):
        return os.path.split(file_path)[1]

    def move_files(self):
        for file_path in self.documents_paths:
            full_new_file_path = os.path.join(
                self.client_documents_folder_path, file_path)
            shutil.move(file_path, full_new_file_path)
            self.full_moved_file_paths.append(full_new_file_path)

    def create_client(self):
        self.get_form_data()
        self.create_client_document_folder()
        self.move_client_documents()
        self.save_client_to_db()
        self.close_sqlite_connection()
        self.switch_layout(Layouts.CLIENT_LIST)

    def switch_layout(self, layout):
        self.load_screen(layout)
        if layout == Layouts.CREATE_CLIENT:
            self.get_columns_properties()
            self.create_additional_widgets()

    def save_client_to_db(self):
        self.create_query()
        self.insert_new_client_to_db()

    def move_client_documents(self):
        self.move_files()
        self.update_documents()

    def create_query(self):
        self.get_additional_query_params()

    def set_up_db(self):
        self.get_sqlite_connection()
        self.create_table_if_doesnt_exist()

    def close_sqlite_connection(self):
        self.con.close()

    def insert_new_client_to_db(self):
        query = SqlParts.INSERT_START.value + self.columns_seperator.join(
            self.columns) + SqlParts.INSERT_MID.value + self.values_placeholders \
            + SqlParts.INSERT_END.value

        self.cur.execute(query, self.form_data)
        self.con.commit()

    def create_table_if_doesnt_exist(self):
        query = self.load_json(self.create_db_query_file_path)
        self.cur.execute(query)
        self.con.commit()

    def get_additional_query_params(self):
        self.values_placeholders = (
            StringParts.QUESTION_MARK_COMMA_SPACE.value * (len(self.columns)))[:-2]
        self.columns_seperator = StringParts.COMMA_SPACE.value

    def get_form_data(self):
        self.form_data = [
            getattr(self, column_name).text()
            if column_name != Names.COMMENTS_COLUMN_NAME.value
            else getattr(self, column_name).toPlainText()
            for column_name in self.columns
        ]

    def get_sqlite_connection(self):
        self.con = sqlite3.connect(Names.DB_NAME.value)
        self.cur = self.con.cursor()


def start_main_program(__name__, Main):
    if __name__ == Names.MAIN_PYTHON_PROCESS.value:
        app = QApplication(sys.argv)
        main = Main()
        main.setMinimumWidth(800)
        main.setMinimumHeight(1000)
        main.show()
        dir(main)
        sys.exit(app.exec())


start_main_program(__name__, Main)
