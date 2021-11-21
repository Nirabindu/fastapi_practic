import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
class Setting:
    title = 'Simple fastapi test project'
    version = '0.0.1'
    description = """
    This apis are just for test that i have learned until now and i do further 
    """
    SQL_USER = os.getenv("sql_user")
    SQL_PASSWORD = os.getenv("sql_pass")
    SQL_SERVER = os.getenv("sql_server")
    SQL_PORT = os.getenv("sql_port")
    SQL_DATABASE = os.getenv("sql_database")
    SQLALCHAMY_DATABASE_URL = f'mysql+mysqlconnector://{SQL_USER}:{SQL_PASSWORD}@{SQL_SERVER}:{SQL_PORT}/{SQL_DATABASE}'
    SECRET_KEY = os.getenv('secret_key')
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 5

setting = Setting()    


