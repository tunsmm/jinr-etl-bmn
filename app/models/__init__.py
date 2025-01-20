from sqlalchemy.ext.declarative import declarative_base

from .domain.enums import STATUS
from .telegram_bot import TelegramBot

# Define a base class for declarative class definitions
Base = declarative_base()
