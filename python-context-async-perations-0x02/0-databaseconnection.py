
import sqlite3 
class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None
    def __enter__ (self):
        self.conn= sqlite3.connect(self.db_name)
        print("Database Connection Established")
        return self.conn
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("Database Connection Closed")
with DatabaseConnection('example.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    ''')
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 25))
    cursor.execute('SELECT * FROM users')
  