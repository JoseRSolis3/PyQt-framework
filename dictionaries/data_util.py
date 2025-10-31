import sqlite3
from log_util import log

# TODO: Column Name Setter

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