import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from .logger import logger

load_dotenv()

DEBUG = os.getenv('DEBUG', 0)

REMOTE_SERVER = os.getenv('REMOTE_SERVER', 'localhost')
REMOTE_USER = os.getenv('REMOTE_USER', 'default_user')

# Путь к директории, которую нужно мониторить
DIRECTORY_TO_MONITOR = "./dir_to_monitor/"
os.makedirs(DIRECTORY_TO_MONITOR, exist_ok=True)

# Путь к директории, куда требуется копировать
REMOTE_DIRECTORY ="./dir_with_copied_files/"
os.makedirs(REMOTE_DIRECTORY, exist_ok=True)

NUMBER_OF_WORKERS_FOR_COPY_FILES = 3

# Аргументы для DAG
DEFAULT_DAG_ARGS = {
    'owner': 'tunsmm',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

META_INFO_FILE_PATH = os.getenv('META_INFO_FILE_PATH', 'meta_info.pickle')
os.makedirs(DIRECTORY_TO_MONITOR, exist_ok=True)

MAIN_DB_USER = os.getenv('MAIN_DB_USER', 'default-123')
MAIN_DB_PASSWORD = os.getenv('MAIN_DB_PASSWORD', 'default-123')
MAIN_DB_HOST = os.getenv('MAIN_DB_HOST', 'default-123')
MAIN_DB_PORT = os.getenv('MAIN_DB_PORT', '5432')
MAIN_DB_NAME = os.getenv('MAIN_DB_NAME', 'default-123')
