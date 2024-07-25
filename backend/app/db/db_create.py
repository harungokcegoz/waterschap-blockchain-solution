import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv("app/db/.env")

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

try:
    conn = psycopg2.connect(
        dbname="postgres", 
        user=DB_USERNAME, 
        password=DB_PASSWORD, 
        host=DB_HOST, 
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
    cursor.execute(create_db_query)

    conn.close()
    conn = psycopg2.connect(
        dbname=DB_NAME, 
        user=DB_USERNAME, 
        password=DB_PASSWORD, 
        host=DB_HOST, 
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    print("\033[92mSCRIPT:    Database created successfully.\033[0m")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_sql_path = os.path.join(script_dir, 'db.sql')

    with open(db_sql_path, 'r') as file:
        queries = file.read()

    cursor.execute(queries)
    print("\033[92mSCRIPT:    Queries executed successfully.\033[0m")

    cursor.close()
    conn.close()

except Exception as e:
    print("\033[91mERROR:   Error creating database:\033[0m", e)
