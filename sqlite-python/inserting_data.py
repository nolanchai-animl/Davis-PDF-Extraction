# Creating SQLite database from a python program
import sqlite3

database = 'ocr_data.db'

def add_project(conn, project):
    # insert table statement
    sql = '''INSERT INTO projects(name, begin_date, end_date)
             VALUES(?,?,?)'''
    
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()

    return cur.lastrowid

def add_task(conn, task):
    sql = '''INSERT INTO tasks(name, priority, status_id, project_id, begin_date, end_date)
             VALUES(?,?,?,?,?,?)'''
    
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

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
def main():   
    try: 
        with sqlite3.connect(database) as conn: # replace database with ':memory:' to create db in memory 
            project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
            project_id = add_project(conn, project)
            print(f'Created a project with the id {project_id}')
            
            tasks = [
                ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02'),
                ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
            ]

            for task in tasks:
                task_id = add_task(conn, task)
                print(f'Created task with the id {task_id}')



    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    main()