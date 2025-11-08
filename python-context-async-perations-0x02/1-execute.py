
import sqlite3
class ExecuteQuery:
    def __init__(self,db_name,query ,params):
        self.query = query
        self.db_name = db_name
        self.conn = None
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__ (self):
        self.conn= sqlite3.connect(self.db_name)
        self.cursor=self.conn.cursor()
        try:
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
        except Exception as e:
            print("Error executing query:", e)
            raise

        return self.results
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        if self.conn:
            self.conn.close()
            print(f"Connection to {self.db_name} closed.")

        return False
with sqlite3.connect("example.db") as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'Alice', 25)")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'Bob', 30)")
    c.execute("INSERT OR IGNORE INTO users VALUES (3, 'Charlie', 35)")
    conn.commit()

query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("example.db", query, params) as results:
    print("\nUsers older than 25:")
    for row in results:
        print(row)
    