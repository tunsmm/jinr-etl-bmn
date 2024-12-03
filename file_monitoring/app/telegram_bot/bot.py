from typing import List, Tuple
import asyncio
import os

from app.dags.models.db import FileCopyHistory
from model import TelegramBot


if __name__ == "__main__":
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'no_token')
    bot = TelegramBot(TOKEN)

    loop = asyncio.get_event_loop()
    
    # Фоновая задача для отправки сообщений
    loop.create_task(bot.periodic_message_sender())

    # Основной цикл обработки сообщений от пользователей
    loop.run_until_complete(bot.start_polling())
