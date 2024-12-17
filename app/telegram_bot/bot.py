import asyncio
import os

from model import TelegramBot
from stats import StatsFlow

if __name__ == "__main__":
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'no_token')
    stats_flow = StatsFlow()
    bot = TelegramBot(TOKEN)

    loop = asyncio.get_event_loop()
    
    # Фоновая задача для отправки сообщений
    loop.create_task(bot.periodic_message_sender(stats_flow.execute_pipeline_methods))

    # Основной цикл обработки сообщений от пользователей
    loop.run_until_complete(bot.start_polling())
