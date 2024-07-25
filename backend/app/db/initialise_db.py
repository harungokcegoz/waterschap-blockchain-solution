import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import subprocess
import platform

def get_python_executable():
    if platform.system() == 'Windows':
        return 'python'
    else:
        return 'python3'

load_dotenv("app/db/.env")

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

conn = psycopg2.connect(
    dbname="postgres",
    user=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
if not cursor.fetchone():
    python_executable = get_python_executable()
    subprocess.run([get_python_executable(), "app/db/db_create.py"])
else:
    print("\033[94mDatabase already exists.\033[0m")
    
cursor.close()
conn.close()
