import sqlite3
from log_util import advanced_log
from dictionaries.builders import class_name
from api_util import Check


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
reservedKeywords = set([
    "select", "where", "order", "create",
    "from", "group", "having", "join",
    "delete", "alter", "update"
])

class Library():
    def __init__(self) -> None:
        self.dataBaseDirectory = set()
        self.tableDirectory = {}
        self.columnDirectory = {}
    
    def tableRegistration(self, tableName: str, value: str):
        if tableName in self.tableDirectory:
            return False
        self.tableDirectory[tableName] = value
        return True
    
    def columnRegistration(self, columnName:str, values: dict):
        if columnName in self.columnDirectory:
            return False
        self.columnDirectory[columnName] = values
        return True
    
    def dataBaseRegistration(self, dataBaseName: str):
        if dataBaseName in self.dataBaseDirectory:
            return False
        self.dataBaseDirectory.add(dataBaseName)
        return True
    
    def search(self, startsWith: str):
       Check.none(startsWith)
       Check.String(startsWith)
       return {
            name: self.tableDirectory[name]
            for name in self.tableDirectory
            if name.startswith(startsWith)
       }

universalLibrary = Library()

class Table():
    @staticmethod
    def create(dataBaseName: str, tableName: str):
        Check.none(dataBaseName, tableName)
        Check.String(dataBaseName, tableName)
        if tableName in reservedKeywords:
            raise NameError(f"{tableName} is a reserved keyword")
        tableName = tableName.strip().lower()
        command = f"""
            CREATE TABLE IF NOT EXISTS {tableName}(
            id INTEGER PRIMARY KEY AUTOINCREMENT
            );
        """
        universalLibrary.tableRegistration(tableName, command)
        Table.commit(dataBaseName, command, None)

    @staticmethod
    def delete(dataBaseName: str, tableName: str):
        Check.none(dataBaseName, tableName, )
        Check.String(dataBaseName, tableName)
        if tableName in universalLibrary.tableDirectory:
            sqlCommand = f"DROP TABLE {tableName}"
            Table.commit(dataBaseName, sqlCommand, None)

    @staticmethod
    def commit(dataBase: str, sqlCommand: str, parameters: tuple | dict | None = None):
        Check.none(dataBase, sqlCommand, parameters)
        Check.String(dataBase, sqlCommand)
        conn = sqlite3.connect(dataBase)
        universalLibrary.dataBaseRegistration(dataBase)
        cursor = conn.cursor()
        if parameters:
            cursor.execute(sqlCommand,parameters)
        else:
            cursor.execute(sqlCommand)
        conn.commit()
        conn.close()

class Column():
    dataTypes ={
    int : "INTEGER",
    float : "REAL",
    str : "TEXT",
    bytes : "BLOB",
    bool : "INTEGER",
    type(None) : "NULL"}

    @staticmethod
    def data(columnName: str, dataType):
        Check.none(columnName, dataType)
        if dataType in Column.dataTypes:
            sqlType = Column.dataTypes[dataType]
            Check.String(columnName, sqlType)
        else:
            Check.String(columnName)
        if columnName not in universalLibrary.columnDirectory:
            raise LookupError(f"{columnName} does not exist.")
        return {columnName : sqlType}


    @staticmethod
    def insert(dataBaseName: str, tableName: str, data: dict):
        Check.none(dataBaseName, tableName, data)
        Check.String(dataBaseName, tableName)
        Check.Dictionary(data)
        for columnName, sqlType in data.items():
            name = columnName.strip().lower()
            if name in reservedKeywords:
                raise NameError(f"{name} is a reserved keyword.")
            command = f"""
                ALTER TABLE {tableName}
                ADD COLUMN {name} {sqlType} NOT NULL;
            """
            Table.commit(dataBaseName, command, None)