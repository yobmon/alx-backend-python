
seed = __import__('seed')
def stream_user_ages():

    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        
        cursor.execute("SELECT age FROM alx_users;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]
        cursor.close()
    except Exception as e:
        print("❌ Failed to compute ages:", e)


def stream_average_user_ages():
    total_age=0
    count=0
    for age in stream_user_ages():
        total_age += age
        count += 1
        average_age= total_age / count
    yield average_age
