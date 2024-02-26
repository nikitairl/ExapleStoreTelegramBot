from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, or_f

from filters.chats import ChatTypeFilter
from keyboards.reply import start_kb, del_kb

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def on_start(message: types.Message):
    await message.answer(
        f"Hello {message.from_user.first_name}! How can I help you?",
        reply_markup=start_kb,
    )


@user_private_router.message(or_f(Command("menu"), F.text.lower() == "menu"))
async def menu_handler(message: types.Message):
    await message.answer("Menu", reply_markup=del_kb)


@user_private_router.message(Command("about"))
@user_private_router.message(F.text.lower().contains("about"))
async def about_handler(message: types.Message):
    await message.answer("About")


@user_private_router.message(Command("payment"))
@user_private_router.message(F.text.lower().contains("payment"))
async def payment_handler(message: types.Message):
    await message.answer("Payment")


@user_private_router.message(Command("feedback"))
@user_private_router.message(F.text.lower().contains("feedback"))
async def feedback_handler(message: types.Message):
    await message.answer("Feedback")


@user_private_router.message(Command("shipping"))
@user_private_router.message(
    (F.text.lower().contains("shipping methods"))
    | (F.text.lower() == "shipping info")
)
async def menu_cmd(message: types.Message):
    await message.answer("Here are  the available shipping methods")
