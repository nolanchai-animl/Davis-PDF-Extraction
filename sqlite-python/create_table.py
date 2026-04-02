# Creating SQLite database from a python program
import sqlite3

database = 'ocr_data.db'
#create_table = 'pytesseract_data'

# Table Example
sql_statements = [
    """CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        name text NOT NULL,
        begin_date DATE,
        end_date DATE
    );""",

    """CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name text NOT NULL,
        priority INT,
        project_id INT NOT NULL,
        status_id INT NOT NULL,
        begin_date DATE NOT NULL,
        end_date DATE NOT NULL,
        FOREIGN KEY (project_id)
        REFERENCES projects (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );"""
]

try: 
    with sqlite3.connect(database) as conn: # replace database with ':memory:' to create db in memory 
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.") # won't need this later (verifies database was created)
        
        # Creating table
        cursor = conn.cursor()

        # execute statements
        for statement in sql_statements:
            cursor.execute(statement)

        # commit changes    
        conn.commit()

        print("Tables created successfully.")

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)