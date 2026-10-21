import os
from pathlib import Path 
from dotenv import load_dotenv 

project_folder = Path(__file__).parent 

env_file = project_folder / "notebooks" / ".env" 

load_dotenv(env_file)

schema = "Library"
host = "127.0.0.1"
user = "root"
password = os.getenv("MYSQL_PASSWORD")
port = 3306

connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}"