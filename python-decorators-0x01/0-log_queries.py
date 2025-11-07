import sqlite3
import functools
from datetime import datetime

def with_db_connection(func):
    @functools.wraps(func)

    def wrapper(*args, **kwargs):
        conn= sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = kwargs.get('query', None)
        if query:
            print(f"[LOG] Executing SQL Query: {query} at {currenttime} time")
        else:
            print("[LOG] No query provided.")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
)
""")
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users(query="SELECT * FROM users")
