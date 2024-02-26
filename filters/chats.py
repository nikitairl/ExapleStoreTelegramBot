from aiogram.filters import Filter
from aiogram import types


class ChatTypeFilter(Filter):
    def __init__(self, chats: list[str]):
        self.chats = chats

    async def __call__(self, message: types.Message):
        return message.chat.type in self.chats
