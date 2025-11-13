import sqlite3
from log_util import advanced_log
from dictionaries.builders import class_name


# TODO: Column Name Setter
# TODO: Validate column syntax (ensure each entry contains a name and type)
# TODO: Allow dynamic table alterations (add new columns if table already exists)
# TODO: Add type checking for db_name and table_name inputs
# TODO: Support passing columns as a dict {name: type} in addition to list/tuple
# TODO: Detect and prevent SQL injection via unsafe table/column names
# TODO: Provide an option to skip auto-creation (manual mode)
# TODO: Add logging for table creation status (created vs already existed)
# TODO: Enable wrapper to return cursor or connection if user needs deeper DB operations
# TODO: Add docstring + usage examples for the decorator
# TODO: Create a unified error-handling system for SQLite exceptions
# TODO: Add unit tests for wrapper behavior
# TODO: Add optional parameter for enabling/disabling AUTOINCREMENT primary key
# TODO: Integrate with upcoming verifier wrapper (auto sanity-check arguments)
# TODO: Add support for foreign keys and constraints in column definitions
# TODO: Add caching so the same table isn't re-validated on every call
# TODO: Add async version in the future when framework grows
# TODO: Possibly support multiple tables per decorator call

default_text = "Enter Text Here"

def table_creation(table_name, column):
    initial = "CREATE TABLE IF NOT EXISTS"
    title_setter = lambda n: initial + f" {n}"
    default_column = "id INTEGER PRIMARY KEY AUTOINCREMENT"

    if table_name is None:
        advanced_log("info",f"Table needs a name to initiate. Setting default text.")
        initial = title_setter(default_text)
    elif isinstance(table_name, str):
        table_name = table_name.strip()
        advanced_log("info",f"Table name validated! Adding it to table.")
        initial = title_setter(table_name)
    else:
        advanced_log("warning",f"Invalid data type: {class_name(table_name)}. Setting default text.")
        initial = title_setter(default_text)

def columns(col_name, data_type, **constraints):
    
    data_types = {
        "int" : "INTEGER",
        "float" : "REAL",
        "str" : "TEXT",
        "bytes" : "BLOB",
        "bool" : "INTEGER",
        "NoneType" : "NULL"
    }

    if col_name is None:
        advanced_log("warning",f"Column Name is None. Please add a name to the column. Setting default text.")
        col_name = default_text
    elif isinstance(col_name, str):
        col_name.strip()
        advanced_log("info",f"Column title validated. Setting column title to {col_name}")
    else:
        advanced_log("warning",f"Invalid data type: {class_name(col_name)}. Setting default text.")
        col_name = default_text
    
    if data_type is None:
        advanced_log("warning",f"data type is empty. Please enter data type. Setting default.")
        data_type = "TEXT"
    elif isinstance(data_type, str):
        data_type = data_type.strip().lower()
        if data_type in data_types:
            verified_type = data_types[data_type]
            advanced_log("info","")