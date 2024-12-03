import asyncio
import json

from aiogram import Bot, Dispatcher, types

class TelegramBot:
    def __init__(self, token, allowed_users: set = set()):
        self.token = token
        if isinstance(allowed_users, set): 
            self.allowed_users = allowed_users
        else:
            self.load_users()
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()

        # Регистрация обработчиков
        self.dp.message.register(self.handle_message)

    def load_users(self):
        """Загружает идентификаторы пользователей из файла."""
        try:
            with open('users.json', 'r') as f:
                self.allowed_users = set(json.load(f))
        except FileNotFoundError:
            self.allowed_users = set()

    def save_user(self, user_id):
        """Сохраняет идентификатор пользователя в файл."""
        if user_id not in self.allowed_users:
            self.allowed_users.add(user_id)
            with open('users.json', 'w') as f:
                json.dump(list(self.allowed_users), f)

    async def send_message_to_all(self, message):
        """Отправляет сообщение всем пользователям."""
        for user_id in self.allowed_users:
            await self.send_message(user_id, message)

    async def send_message(self, chat_id, message):
        """Отправляет сообщение пользователю."""
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
            print(f"Сообщение отправлено в {chat_id}: {message}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

    async def handle_message(self, message: types.Message):
        """Обрабатывает входящие сообщения."""
        user_id = message.from_user.id
        self.save_user(user_id)  # Сохраняем пользователя при любом сообщении

        # Пример простого ответа
        await self.send_message(user_id, "Ваше сообщение получено!")

    async def periodic_message_sender(self):
        """Отправляет сообщение всем пользователям каждую минуту."""
        while True:
            await self.send_message_to_all("Это сообщение отправлено всем пользователям каждую минуту.")
            await asyncio.sleep(60)

    async def start_polling(self):
        """Запускает поллинг."""
        await self.dp.start_polling(self.bot)
