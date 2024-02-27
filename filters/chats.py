from aiogram.filters import Filter
from aiogram import types, Bot


class ChatTypeFilter(Filter):
    def __init__(self, chats: list[str]):
        self.chats = chats

    async def __call__(self, message: types.Message):
        return message.chat.type in self.chats


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_admins_list
