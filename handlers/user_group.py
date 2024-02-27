from string import punctuation

from aiogram import types, Router, Bot
from aiogram.filters import Command

from filters.chats import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter([
    'group', 'supergroup'
]))
user_group_router.edited_message.filter(ChatTypeFilter([
    'group', 'supergroup'
]))


@user_group_router.message(Command("admin"))
async def admin(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == 'creator' or member.status == 'administrator'
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    print(admins_list)

restricted_words = {'bitch'}


def clean_text(text: str) -> str:
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def moderation(message: types.Message):
    if restricted_words.intersection(clean_text(message.text).lower().split()):
        await message.answer(f"{message.from_user.first_name} - behave! 🤬")
        await message.delete()
