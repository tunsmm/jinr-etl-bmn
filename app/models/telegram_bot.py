import asyncio
import json

from aiogram import Bot, Dispatcher, types
from airflow.models import Variable

from config.logger import logger


class TelegramBot:
    def __init__(self, token, allowed_users: set = None):
        self.token = token
        config_allowed_users = Variable.get("allowed_tg_users", default_var=None)
        if isinstance(allowed_users, set): 
            self.allowed_users = allowed_users
        elif config_allowed_users:
            self.allowed_users = config_allowed_users
        else:
            self.load_users()
            Variable.set(
                "allowed_tg_users",
                self.allowed_users,
                "The list of telegram user IDS to whom bot will send notifications.",
            )

        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()

        # Register handlers
        self.dp.message.register(self.handle_message)

    def load_users(self):
        """Load user telegram IDs from a file."""
        file_name = 'users.json'
        try:
            with open(file_name, 'r') as f:
                self.allowed_users = set(json.load(f))
                logger.info(f'allowed_users from {file_name} is {self.allowed_users}')
        except FileNotFoundError:
            logger.error(f'{file_name} is not found')
            self.allowed_users = set()

    def save_user(self, user_id):
        self.allowed_users.add(user_id)
        with open('users.json', 'w') as f:
            json.dump(list(self.allowed_users), f)

    async def send_message_to_all(self, message, file=None):
        for user_id in self.allowed_users:
            await self.send_message(user_id, message, file)

    async def send_message(self, chat_id, message, file=None):
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
            if file:
                await self.bot.send_document(chat_id=chat_id, document=file)
            logger.info(f"Message sent to {chat_id}: {message}")
        except Exception as e:
            logger.info(f"Error sending message: {e}")

    async def handle_message(self, message: types.Message):
        user_id = message.from_user.id
        if user_id not in self.allowed_users:
            self.save_user(user_id)  # Save the user upon any message
            await self.send_message(user_id, "You have been added to the recipient list.")

    async def periodic_message_sender(self, pipeline_method):
        """Send a message to all users every minute."""
        while True:
            for function in pipeline_method():
                message, file = function()
                if message:
                    logger.info(f'{function.__name__} message is {message}; file is {file}')
                    await self.send_message_to_all(message, file)

            await asyncio.sleep(60)

    async def start_polling(self):
        await self.dp.start_polling(self.bot)
