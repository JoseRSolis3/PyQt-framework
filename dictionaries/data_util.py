import sqlite3
from log_util import log

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

def table_builder_wrapper(db_name, table_name, columns):
    def decorator(func):
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            clean_name = table_name.strip().lower()

            if isinstance(columns, (list, tuple)):
                if columns == []:
                    log.warning(f"Columns list is empty. Returning None")
                    return None
                if columns:
                    column_converted = ",\n".join(columns)
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {clean_name}(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            {column_converted}
                        )
                    """)
            
            conn.commit()
            
            result = func(*args, **kwargs)
            conn.close()
            return result
        
        return wrapper
    return decorator