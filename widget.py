# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import shutil
import sys
from PySide6 import QtGui
from PySide6 import QtCore

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

import sqlite3

from pprint import pprint


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        self.get_column_names()
        self.get_base_dir()
        self.get_documents_dir()
        self.init_new_filepaths_property()
        self.load_ui()

    def create_client_document_folder(self):
        self.create_client_documents_folder_name()
        self.create_client_document_folder_path()
        os.mkdir(self.client_documents_folder_path)

    def create_client_document_folder_path(self):
        self.client_documents_folder_path = os.path.join(self.base_dir, self.documents_dir, self.client_documents_folder_name)

    def create_client_documents_folder_name(self):
        self.client_documents_folder_name = f'{self.form_data[0]}-{self.form_data[1]}-{self.form_data[2]}'

    def init_new_filepaths_property(self):
        self.moved_filenames = []

    def get_documents_dir(self):
        self.documents_dir = 'files'

    def get_base_dir(self):
        self.base_dir = os.getcwd()

    def get_column_names(self):
        self.columns = [
            'first_name',
            'last_name',
            'passport_no',
            'national_id',
            'address',
            'employer1',
            'employer2',
            'comments',
            'documents'
        ]

    def load_ui(self):
        loader = QUiLoader()
        path = self.get_main_screen_file_path()
        ui_file = self.load_main_screen_file(loader, path)
        self.close_main_screen_file(ui_file)
        self.get_columns_properties()
        self.create_additional_widgets()
        
        # for dev only - remove after
        self.fill_in_form()
        # for dev only - remove after

        self.add_icon_to_button()

    def get_columns_properties(self):
        for column_name in self.columns:
            setattr(self, column_name, getattr(self.ui, column_name))

    def close_main_screen_file(self, ui_file):
        ui_file.close()

    def create_additional_widgets(self):
        self.create_client_button = self.ui.create_client_button
        self.create_client_button.clicked.connect(self.create_client)
        self.documents_button = self.ui.documents_button
        self.documents_button.clicked.connect(self.select_documents)
        self.documents.hide()

    def load_main_screen_file(self, loader, path):
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        return ui_file

    def get_main_screen_file_path(self):
        return os.fspath(Path(__file__).resolve().parent / "form.ui")

    def add_icon_to_button(self):
        self.documents_button.setIcon(QtGui.QIcon('file-line.svg'))
        self.documents_button.setIconSize(QtCore.QSize(24, 24))

    def fill_in_form(self):
        self.first_name.setText('אריאל')
        self.last_name.setText('פרדמן')
        self.passport_no.setText('350186548')
        self.national_id.setText('066423872')
        self.address.setText('אחד העם 1 ב רחובות 7626103')
        self.employer1.setText('לרה יעקב')
        self.employer2.setText('עזרה סוכנות כוח אדם בע"מ')
        self.comments.setText('סוכם שהתוכנה תסופק הערב')

    def select_documents(self):
        self.get_documents_paths()

    def get_documents_paths(self):
        self.documents_paths = QFileDialog.getOpenFileNames()[0]

    def update_documents(self):
        self.documents.setText(''.join(
            os.path.join(self.client_documents_folder_path, filename)
            for filename in self.get_documents_filenames()
        ))

    def get_documents_filenames(self):
        return [self.get_filename(file_path) for file_path in self.documents_paths]

    def get_filename(self, file_path):
        return os.path.split(file_path)[1]

    def move_files(self):
        for file_path in self.documents_paths:
            shutil.move(file_path, self.client_documents_folder_path)

    def create_client(self):
        self.set_up_db()
        self.save_client_to_db()
        self.create_client_document_folder()
        self.move_client_documents()
        self.close_sqlite_connection()

    def save_client_to_db(self):
        self.create_query()
        self.insert_new_client_to_db()

    def move_client_documents(self):
        self.move_files()
        self.update_documents()

    def create_query(self):
        self.get_form_data()
        self.get_additional_query_params()

    def set_up_db(self):
        self.get_sqlite_connection()
        self.create_table_if_doesnt_exist()

    def close_sqlite_connection(self):
        self.con.close()

    def insert_new_client_to_db(self):
        query = f'insert into clients({self.columns_seperator.join(self.columns)}) values ({self.values_placeholders})'

        self.cur.execute(query, self.form_data)
        self.con.commit()

    def create_table_if_doesnt_exist(self):
        query = \
            '''
            create table if not exists clients(
            id integer primary key autoincrement,
            first_name text,
            last_name text,
            passport_no text,
            national_id text,
            address text,
            employer1 text,
            employer2 text,
            comments text,
            documents text
            )
        '''
        self.cur.execute(query)
        self.con.commit()

    def get_additional_query_params(self):
        self.values_placeholders = ('?, ' * (len(self.columns)))[:-2]
        self.columns_seperator = ', '

    def get_form_data(self):
        self.form_data = [
            getattr(self, column_name).text()
            if column_name != 'comments'
            else getattr(self, column_name).toPlainText()
            for column_name in self.columns
        ]

    def get_sqlite_connection(self):
        self.con = sqlite3.connect('simplecm.db')
        self.cur = self.con.cursor()


def start_main_program(__name__, Main):
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        main = Main()
        main.setMinimumWidth(800)
        main.setMinimumHeight(1000)
        main.show()
        dir(main)
        sys.exit(app.exec())

start_main_program(__name__, Main)
