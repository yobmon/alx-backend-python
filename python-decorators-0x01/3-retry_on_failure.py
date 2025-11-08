import time
import functools


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
def setup_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """)
    cursor.executemany(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        [("Alice", 30), ("Bob", 25)]
    )
    conn.commit()
    print("✅ Database initialized with sample users.")

def retry_on_failure(retries=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            
            attempt = 0
            while attempt < retries:
                try:
                    result = func(conn, *args, **kwargs)
                    conn.commit()
                    print(f"✅ Transaction committed (attempt {attempt + 1})")
                    return result
                except sqlite3.OperationalError as e:
                    print(f"⚠️ Transient DB error: {e}. Retrying in {delay} sec...")
                    conn.rollback()
                    attempt += 1
                    time.sleep(delay)
                except Exception as e:
                    conn.rollback()
                    print(f"❌ Transaction rolled back due to error: {e}")
                    raise
            raise Exception("❌ Transaction failed after multiple retries.")
        return wrapper
    return decorator

@with_db_connection

@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    setup_db(conn)  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)