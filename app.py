import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from dotenv import load_dotenv

from constants import ALLOWED, PRIVATE_MENU
from db.db import create_db, drop_db, session_maker
from handlers.admin_private import admin_router
from handlers.user_group import user_group_router
from handlers.user_private import user_private_router
from middlewares.db_middleware import DataBaseSession

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
bot.my_admins_list = []

dp: any = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)


async def on_startup():
    run_param = False
    if run_param:
        await drop_db()
    await create_db()


async def on_shutdown():
    print('Bot is shutting down...')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=PRIVATE_MENU,
        scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED)

asyncio.run(main())
