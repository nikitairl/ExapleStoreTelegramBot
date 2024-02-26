from string import punctuation

from aiogram import types, Router

from filters.chats import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter([
    'private', 'group', 'supergroup'
]))


restricted_words = {'bitch'}


def clean_text(text: str) -> str:
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def moderation(message: types.Message):
    if restricted_words.intersection(clean_text(message.text).lower().split()):
        await message.answer(f"{message.from_user.first_name} - behave! 🤬")
        await message.delete()
