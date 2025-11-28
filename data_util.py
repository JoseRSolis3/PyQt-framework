import sqlite3
from log_util import advanced_log
from dictionaries.builders import class_name, cleaner, loweredCleaner
from api_util import Check
import os


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
        self.dataBaseDirectory = {}
        self.tableDirectory = {}
        self.columnDirectory = {}

    def startsWith(self, itemName:str, search:str):
        cleanedItem = loweredCleaner(itemName)
        cleanedName = loweredCleaner(search)
        return cleanedItem.startswith(cleanedName)
        
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
    
    def dataBaseRegistration(self, dataBaseName: str | dict, connection):
        if isinstance(dataBaseName, dict):
            for folder, file in dataBaseName.items():
                if folder not in self.dataBaseDirectory:
                    self.dataBaseDirectory[folder] = {}
                self.dataBaseDirectory[folder][file] = connection
        if isinstance(dataBaseName, str):
            self.dataBaseDirectory[dataBaseName] = connection
        return True
    
    def search(self, startsWith: str, dataBase = False, tables = False, columns = False):
        Check.none(startsWith)
        Check.String(startsWith)
        if dataBase:
            directory = self.dataBaseDirectory
        elif tables:
            directory = self.tableDirectory
        elif columns:
            directory = self.columnDirectory
        else:
            directory = self.tableDirectory

        return {
            name: directory[name]
            for name in directory
            if name.startswith(startsWith)
       }

dataLibrary = Library()

class DataBase():
    @staticmethod
    def create(folderName:str, dataBaseName: str, folder = False):
        Check.none(dataBaseName)
        Check.String(dataBaseName, folderName)
        cleanedFolder = loweredCleaner(folderName)
        cleanedFile = loweredCleaner(dataBaseName)

        if not cleanedFile.endswith(".db"):
            advanced_log("info",f"{cleanedFile} is missing '.db'. Adding it to name.")
            cleanedFile += ".db"

        if folder == True:
            directory = os.path.join(cleanedFolder, cleanedFile)
            folderLocation = os.path.dirname(directory)
        else:
            folderLocation = os.path.dirname(os.path.join("data",cleanedFile))

        if folderLocation and not os.path.exists(folderLocation):
            advanced_log("info",f"{folderLocation} does not exist. Creating {folderLocation} location.")
            os.makedirs(folderLocation)
        path = os.path.join(folderLocation, cleanedFile)
        conn = sqlite3.connect(path)
        registered = dataLibrary.dataBaseRegistration({folderLocation:cleanedFile}, conn)
        return conn if registered else None
    
class Table():
    @staticmethod
    def create(dataBaseName: str, tableName: str):
        advanced_log("debug",f"RAW DATA | data base: {dataBaseName}. table: {tableName}")
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
        advanced_log("info",f"{command}")
        dataLibrary.tableRegistration(tableName, command)
        Table.commit(dataBaseName, command, None)

    @staticmethod
    def delete(dataBaseName: str, tableName: str):
        Check.none(dataBaseName, tableName, )
        Check.String(dataBaseName, tableName)
        if tableName in dataLibrary.tableDirectory:
            sqlCommand = f"DROP TABLE {tableName}"
            Table.commit(dataBaseName, sqlCommand, None)

    @staticmethod
    def commit(dataBase: str, sqlCommand: str, parameters: tuple | dict | None = None):
        Check.none(dataBase, sqlCommand)
        Check.String(dataBase, sqlCommand)
        cleanedDataBase = loweredCleaner(dataBase)
        conn: sqlite3.Connection | None = None
        for folder,files in dataLibrary.dataBaseDirectory.items():
            if cleanedDataBase in files:
                advanced_log("debug",f"Database exists in Directory. Getting.")
                conn = dataLibrary.dataBaseDirectory[folder][cleanedDataBase]
                break
        if conn == None:
            conn = DataBase.create("", cleanedDataBase)
            dataLibrary.dataBaseRegistration(cleanedDataBase, conn)
        assert conn is not None
        advanced_log("info",f"Connected to Data Base.")
        cursor = conn.cursor()
        if parameters:
            cursor.execute(sqlCommand,parameters)
        else:
            cursor.execute(sqlCommand)
        advanced_log("info",f"Commiting: {sqlCommand} with parameters: {parameters} to {dataBase}")
        conn.commit()

class Column():
    integer = "INTEGER"
    real = "REAL"
    text = "TEXT"
    blob = "BLOB"
    switch = "INTEGER"
    null = "NULL"

    dataTypes = [integer, real, text, blob, switch, null]

    @staticmethod
    def data(columnName: str, dataType):
        Check.none(columnName, dataType)
        if dataType in Column.dataTypes:
            Check.String(columnName, dataType)
        else:
            Check.String(columnName)
        if columnName not in dataLibrary.columnDirectory:
            raise LookupError(f"{columnName} does not exist.")
        return {columnName : dataType}

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

class Data():
    @staticmethod
    def insert(dataBaseName: str, tableName:str, data:dict):
        Check.none(dataBaseName, tableName, data)
        Check.String(dataBaseName, tableName)
        Check.Dictionary(data)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        sqlCommand = f"INSERT INTO {tableName} ({columns}) VALUES ({placeholders})"
        Table.commit(dataBaseName, sqlCommand, values)

# Create database
DataBase.create("data", "database1", folder=True)

# Create table
Table.create("database1.db", "table1")

# Add columns
Column.insert("database1.db", "table1", {"name": Column.text, "age": Column.integer})

# Insert data
Data.insert("database1.db", "table1", {"name": "Alice", "age": 30})
Data.insert("database1.db", "table1", {"name": "Bob", "age": 25})
