import subprocess
import platform

def install_dependencies():
    subprocess.run([get_python_executable(), "-m", "pip", "install", "pipreqs"])
    subprocess.run([get_python_executable(), "-m", "pipreqs", "."])
    subprocess.run([get_python_executable(), "-m", "pip", "install", "psycopg2-binary"])
    subprocess.run([get_python_executable(), "-m", "pip", "install", "python-jose"])
    subprocess.run([get_python_executable(), "-m", "pip", "install", "passlib"])
    subprocess.run([get_python_executable(), "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.run([get_python_executable(), "-m", "pip", "install", "uvicorn"])
    subprocess.run([get_python_executable(), "-m", "pip", "install", "pytest"])

def initialize_database():
    subprocess.run([get_python_executable(), "app/db/initialise_db.py"])

def run_server():
    subprocess.run(["uvicorn", "app.main:app", "--reload"])

def get_python_executable():
    if platform.system() == 'Windows':
        return 'python'
    else:
        return 'python3'

if __name__ == "__main__":
    install_dependencies()
    initialize_database()
    run_server()
