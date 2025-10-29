import sqlite3
from sqlite3 import Connection, Cursor
from log_util import log



class userTable:
    def __init__(self):
        pass

    def name_validator(self,table_name: str):
        default_table_name = "Add_Table_Name"
        if isinstance(table_name, str):
            table_name = table_name.strip()
        else:
            log.warning("Table must be a string and must not contain leading or trailing spaces.")
            log.info(f"Using default table name: {default_table_name}")
            table_name = default_table_name
            
        if not isinstance(table_name, str):
            log.error("Table name must be a string.")
            log.info(f"Using default table name: {default_table_name}")
            table_name = default_table_name        
        elif not table_name:
            log.warning("Please provide a valid table name.")
            log.info(f"Using default table name: {default_table_name}")
            table_name = default_table_name
        elif " " in table_name:
            log.warning("Table name cannot contain spaces.")
            log.info(f"Using default table name: {default_table_name}")
            table_name = default_table_name
        elif not table_name.isidentifier():
            log.error("Table name must be a valid identifier (no special characters).")
            log.info(f"Using default table name: {default_table_name}")
            table_name = default_table_name
        else: 
            table_name = table_name.lower()
            log.debug(f"Table name '{table_name}' is valid.")
        return table_name

    def build_user_table(self, table_name: str):
        name = self.name_validator(table_name)
        keys = {
            "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
            "first_name" : "TEXT NOT NULL",
            "last_name" : "TEXT NOT NULL",
            "username" : "TEXT NOT NULL UNIQUE",
            "phone_number" : "TEXT NOT NULL UNIQUE",
            "dob" : "DATE NOT NULL",
            "email" : "TEXT NOT NULL UNIQUE",
            "password" : "TEXT NOT NULL", 
            "created_at" : "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            }
        
        # Generate the table schema string
        table_schema = ", ".join([f"{key} {value}" for key, value in keys.items()])
        try:
           initialize_table = f'''CREATE TABLE IF NOT EXISTS {name} ({table_schema})'''
           log.debug(f"Table schema for {name} initialized successfully.")
        except Exception as e:
            log.error(f"Error initializing table schema for {name}: {e}")
        return initialize_table