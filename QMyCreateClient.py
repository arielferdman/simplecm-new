import json
import os
import shutil
import sqlite3
import sys

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QFileDialog

from MyEnums import (DataFileNames, DirNames, Layouts, Names,
                     SqlParts, StringParts)
from QMyBaseWindow import QMyBaseWindow


class QMyCreateClient(QMyBaseWindow):
    def __init__(self, parent=None):
        super(QMyCreateClient, self).__init__()
        self.init_properties()
        self.load_ui()

    def init_layout(self):
        self.layout = Layouts.CREATE_CLIENT.value

    def init_initial_form_data_file_path(self):
        self.initial_form_data_file_path = os.path.join(
            self.base_path, DataFileNames.INITIAL_FORM_DATA.value)

    def create_client_document_folder(self):
        self.create_client_documents_folder_name()
        self.create_client_document_folder_path()
        if not os.path.exists(self.client_documents_folder_path):
            os.mkdir(self.client_documents_folder_path)

    def create_client_document_folder_path(self):
        self.client_documents_folder_path = os.path.join(
            self.base_path, self.documents_dir, self.client_documents_folder_name)

    def create_client_documents_folder_name(self):
        self.client_documents_folder_name = \
            f'{self.form_data[0]}-{self.form_data[1]}-{self.form_data[2]}'

    def init_new_filepaths_property(self):
        self.full_moved_file_paths = []

    def init_documents_dir(self):
        self.documents_dir = DirNames.CLIENT_DOCUMENTS_DIR.value

    def get_columns_properties(self):
        for column_name in self.columns:
            setattr(self, column_name, getattr(self.ui, column_name))

    def create_additional_widgets(self):
        self.create_client_button = self.ui.create_client_button
        self.create_client_button.clicked.connect(self.create_client)
        self.documents_button = self.ui.documents_button
        self.documents_button.clicked.connect(self.select_documents)
        self.documents.hide()

    def add_icon_to_button(self):
        self.documents_button.setIcon(
            QtGui.QIcon(DataFileNames.DOCUMENT_ICON.value))
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

    def insert_new_client_to_db(self):
        query = SqlParts.INSERT_START.value + self.columns_seperator.join(
            self.columns) + SqlParts.INSERT_MID.value + self.values_placeholders \
            + SqlParts.INSERT_END.value

        self.cur.execute(query, self.form_data)
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
