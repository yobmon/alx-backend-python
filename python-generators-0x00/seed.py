import psycopg2
import csv
CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "1234",
    "port": 5432
}
DB_CONFIG={


    "host": "localhost",
"database": "mydb",
    "user": "postgres",
    "password": "1234",
    "port": 5432



}
def connect_db():
    try:
       conn = psycopg2.connect(**CONFIG)
       print("✅ Connected to PostgreSQL successfully!")
       return conn
    except Exception as e:
       print("❌ Connection failed:", e)
def  connect_to_prodev():
    try:
       conn = psycopg2.connect(**DB_CONFIG)
       print("✅ Connected to ALX_prodev database successfully!")
       return conn
    except Exception as e:
       print("❌ Connection failed:", e)  
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except Exception as e:
        print("❌ Connection failed:", e)   
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
      CREATE TABLE IF NOT EXISTS alx_users (
    user_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age NUMERIC NOT NULL
);
        """)
        connection.commit()
        cursor.close()
        print("✅ Table created successfully!")
    except Exception as e:
        print("❌ Table creation failed:", e)
      


def insert_data(connection, csv_file):
    try:
        cursor =connection.cursor()
        with open(csv_file, 'r',encoding="utf-8") as file:
            reader=csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO alx_users (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_id) DO NOTHING;
                """, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")
    except Exception as err:
        print(f"Error inserting data: {err}")
   
        