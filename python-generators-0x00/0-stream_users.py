
seed = __import__('seed')

def stream_users():
    try:

        connection = seed.connect_db()


        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM alx_users;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break

        
            yield row
        cursor.close()
    except Exception as e:
        print("❌ Failed to stream users:", e)