import sqlite3
from log_util import advanced_log
from dictionaries.builders import class_name, Text
from api_util import Check
import os
from typing import TypedDict


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

default_text = "Enter Text Here"
errorMessage = f"User entered reserved keywords for title. Please rename."
reservedKeywords = set([
    "select", "where", "order", "create",
    "from", "group", "having", "join",
    "delete", "alter", "update"
])

class dataDict(TypedDict):
    folderName : str
    fileName : str
    tableName : str
    command : str

class Library():
    dataBaseDirectory = {}

    def dataBaseRegistration(self, dataBaseName: str | dict, connection):
        if isinstance(dataBaseName, dict):
            for folder, file in dataBaseName.items():
                if folder not in self.dataBaseDirectory:
                    self.dataBaseDirectory[folder] = {}
                self.dataBaseDirectory[folder][file] = connection
        if isinstance(dataBaseName, str):
            self.dataBaseDirectory[dataBaseName] = connection
        return True
    
    def tableRegistration(self, location: dict[str, dict[str, str]], table, connection):
        if isinstance(location, dict):
            for folder, file in location.items():
                if folder not in self.dataBaseDirectory:
                    Library.dataBaseRegistration(self, {folder:file}, connection)
                if isinstance(file, dict):
                    for dataBase, data in file.items():
                        self.dataBaseDirectory[folder][dataBase][connection] = data
                else:
                    raise TypeError(f"Invalid data type. Expected type: dict. Given type: {class_name(file)}")
        else:
            raise TypeError(f"Invalid data type. Expected type: dict. Given type: {class_name(location)}")

dataBase = Library()

class Table:
    def __init__(self, db: "DataBase", tableName: str):
        self.db = db  
        self.name = Text.lowerCasedStrip(tableName)[0]  

    def insert(self, dataValues: dict[str, str]):
        self.db.dataInsert(self.name, dataValues)


class DataBase():
    def __init__(self, folderName:str, fileName:str, customFolder) -> None:
        Check.none(folderName, fileName, exception=True)
        Check.String(folderName, fileName, exception=True)
        self.folder,self.file = Text.lowerCasedStrip(folderName, fileName)
        self.tables = []
        self.columns = {}
        self.secureData = {}
        self.dataTypes = ["INTEGER", "REAL", "TEXT", "BLOB", "NULL"]

    def table(self, tableName: str) -> Table:
            return Table(self, tableName)

    def checkDataType(self, dataType:str)->str:
        Check.none(dataType)
        Check.String(dataType)
        upperCased = Text.upperCase(dataType)
        if upperCased in self.dataTypes:
            return upperCased
        else:
            raise LookupError(f"{upperCased} is not a SQLite data type.")

    def create(self):
        if not self.file.endswith(".db"):
            self.file += ".db"
        customFolder = self.folder
        default = "data"

        if os.path.exists(customFolder):
            base = customFolder
        elif os.path.exists(default):
            base = default
        else:
            base = customFolder
        
        folderLocation = base   
        i = 0
        while os.path.exists(folderLocation):
            i+=1
            folderLocation = f"{base}{i}"
        os.makedirs(folderLocation, exist_ok=True)
        path = os.path.join(folderLocation, self.file)
        conn = sqlite3.connect(path)
        registered = dataBase.dataBaseRegistration({folderLocation:self.file}, conn)
        self.folder = folderLocation
        return conn if registered else None

    def createTable(self,tableName:str, secure= False):
        cleanedTable = Text.strip(tableName)
        if cleanedTable in reservedKeywords:
            raise NameError(f"{tableName} is a reserved keyword")
        command = f"""
            CREATE TABLE IF NOT EXISTS {cleanedTable}(
            id INTEGER PRIMARY KEY AUTOINCREMENT
            );
        """
        print(command)
        connection = dataBase.dataBaseDirectory[self.folder][self.file]
        dataBase.dataBaseRegistration({self.folder: {self.file: cleanedTable}}, connection)
        self.secureData.setdefault(self.file, []).append([cleanedTable, []])
        self.tables.append(cleanedTable)
        self.commit(command)
    
    def createColumn(self, tableName:str, columnName:str, dataType:str):
        Check.none(tableName, columnName, dataType)
        Check.String(tableName, columnName, dataType)
        lowerCasedTitle, lowerCasedColumn = Text.lowerCase(tableName, columnName)
        if columnName in reservedKeywords:
            raise NameError(f"{columnName} is a reserved keyword!")
        if not lowerCasedTitle in self.tables:
            raise ValueError(f"{lowerCasedTitle} does not exist!")
        verifiedData = self.checkDataType(dataType)
        command = f"""
            ALTER TABLE {lowerCasedTitle}
            ADD COLUMN {lowerCasedColumn} {verifiedData} NOT NULL;
        """
        self.columns.setdefault(lowerCasedTitle, []).append(lowerCasedColumn)
        self.secureData.setdefault(self.file, {}).setdefault(lowerCasedTitle, []).append(lowerCasedColumn)
        self.commit(command)
    
    def dataInsert(self, tableName:str, dataValues:dict[str,str]):
        separatedColumnList = []
        separatedValues = []
        for column in dataValues.keys():
            Check.none(column)
            Check.String(column)
            lowerCasedColumn = Text.lowerCase(column)
            separatedColumnList.append(lowerCasedColumn)
        for value in dataValues.values():
            Check.none(value)
            try:
                numberCheck = int(value)
            except:
                try:
                    numberCheck = float(value)
                except:
                    numberCheck = Text.lowerCase(value)
            separatedValues.append(numberCheck)
            
        Check.none(tableName)
        Check.String(tableName)
        lowerCasedTitle= Text.lowerCase(tableName)
        for column in separatedColumnList:
            if not column in self.columns[lowerCasedTitle]:
                raise ValueError(f"{column} does not exist!")
        columns = ", ".join(separatedColumnList)
        placeHolders = ", ".join(["?"] * len(separatedValues))
        values = tuple(separatedValues)
        command = f"""
            INSERT INTO {lowerCasedTitle}
            ({columns}) VALUES ({placeHolders})
        """
        self.commit(command, values)

    def delete(self, tableName:str):
        Check.none(tableName)
        Check.String(tableName)
        lowerCased = Text.lowerCase(tableName)
        if lowerCased in self.tables:
            command = f"""
                DROP TABLE {lowerCased}
            """
            self.commit(command)


    def commit(self, sqlCommand, parameters: tuple | dict | None = None):
            conn = dataBase.dataBaseDirectory[self.folder][self.file]
            cursor = conn.cursor()
            if parameters:
                cursor.execute(sqlCommand, parameters)
            else:
                cursor.execute(sqlCommand)
            conn.commit()

