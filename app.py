import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from constants import ALLOWED, PRIVATE_MENU
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp: any = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)


async def main():
    """
    Asynchronous function that takes a bot object as a parameter and performs
    the following tasks:
    - Deletes the webhook associated with the bot
    - Starts polling for updates using the given bot
    """
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=PRIVATE_MENU,
        scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED)

asyncio.run(main())
