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
errorMessage = f"User entered reserved keywords for title. Please rename."
reservedKeywords = [
    "select", "where", "order", "create",
    "from", "group", "having", "join",
    "delete", "alter", "update"
]

class Table():
    @staticmethod
    def title(title):
        if title is None:
            advanced_log("warning",f"Title is none or empty.")
            raise ValueError("Title is none or empty.")
        elif isinstance(title, str):
            safeTitle = "_".join(title.strip().split()).lower()
            if safeTitle != "":
                advanced_log("info",f"Verified. Setting title as: {safeTitle}")
                if safeTitle in reservedKeywords:
                    advanced_log("warning",errorMessage)
                    raise ValueError(errorMessage)
                return safeTitle
            else:
                advanced_log("warning",f"title is an empty space. Try again.")
                raise ValueError("title is an empty space. Try again.")
        else:
            advanced_log("warning",f"Invalid data type.")
            raise ValueError("Invalid data type.")

class Column():
    int = "INTEGER"
    float = "REAL"
    str = "TEXT"
    bytes = "BLOB"
    bool = "INTEGER"
    NoneType = "NULL"
    create = "CREATE TABLE IF NOT EXISTS"
    mainColumn = "id INTEGER PRIMARY KEY AUTOINCREMENT"

    @staticmethod
    def title(title):
        if title is None:
            advanced_log("warning",f"No title provided Returning empty string.")
            return ""
        elif isinstance(title, str):
            advanced_log("info",f"Title is a string!")
            title = title.strip().lower()
            if title in reservedKeywords:
                advanced_log("warning", errorMessage)
                raise ValueError(errorMessage)
            else:
                return title
        else:
            advanced_log("warning",f"Invalid data type. Returning empty string.")
            return ""