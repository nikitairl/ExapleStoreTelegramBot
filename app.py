import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from dotenv import load_dotenv

from constants import ALLOWED, PRIVATE_MENU
from handlers.user_group import user_group_router
from handlers.user_private import user_private_router
from handlers.admin_private import admin_router

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
bot.my_admins_list = []

dp: any = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)


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




"""
https://www.youtube.com/watch?v=55w2QpPGC-E
23:20
"""