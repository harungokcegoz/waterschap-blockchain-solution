import psycopg2
from dotenv import load_dotenv
import os

load_dotenv("app/db/.env")

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    print("DB_USERNAME:", DB_USERNAME)
    print("DB_PASSWORD:", DB_PASSWORD)
    print("DB_HOST:", DB_HOST)
    print("DB_PORT:", DB_PORT)
    print("DB_NAME:", DB_NAME)

    connection = psycopg2.connect(DATABASE_URL)

    cursor = connection.cursor()

    cursor.execute("SELECT 1")

    result = cursor.fetchone()
    print("Database connected successfully:", result)

    cursor.close()
    connection.close()

except Exception as e:
    print("Error connecting to the database:", e)
