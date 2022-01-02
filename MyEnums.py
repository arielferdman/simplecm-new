from enum import Enum


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
