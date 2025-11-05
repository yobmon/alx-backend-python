
seed = __import__('seed')

def stream_users_in_batches(batch_size):
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM alx_users;")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
        cursor.close()
    except Exception as e:
        print("❌ Failed to stream users in batches:", e)





def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
       filtered_batch= [user for user in batch if user[3] > 25]
       
       return filtered_batch
