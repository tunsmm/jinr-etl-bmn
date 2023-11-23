import os 

from dotenv import load_dotenv

load_dotenv()


REMOTE_SERVER = os.getenv('REMOTE_SERVER', 'localhost')
REMOTE_USER = os.getenv('REMOTE_USER', 'default_user')