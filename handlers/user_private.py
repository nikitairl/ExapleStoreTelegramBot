from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, or_f
from aiogram.utils.formatting import Bold, as_list, as_marked_section

from constants import ABOUT
from filters.chats import ChatTypeFilter
from keyboards.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def on_start(message: types.Message):
    await message.answer(
        f"Hello {message.from_user.first_name}! How can I help you?",
        reply_markup=get_keyboard(
            "Menu",
            "About",
            "Payment info",
            "Shipping info",
            "Feedback",
            placeholder="What do you want?",
            sizes=(2, 3),
        ),
    )


@user_private_router.message(or_f(Command("menu"), F.text.lower() == "menu"))
async def menu_handler(message: types.Message):
    await message.answer("Menu")


@user_private_router.message(Command("about"))
@user_private_router.message(F.text.lower().contains("about"))
async def about_handler(message: types.Message):
    text = as_marked_section(
        Bold("About us:"),
        ABOUT,
    )
    await message.answer(text.as_html())


@user_private_router.message(Command("payment"))
@user_private_router.message(F.text.lower().contains("payment"))
async def payment_handler(message: types.Message):
    text = as_marked_section(
        Bold("Payment methods:"),
        "Card",
        "Cash on delivery",
        "PayPal",
        marker="• ",
    )
    await message.answer(text.as_html())


@user_private_router.message(Command("feedback"))
@user_private_router.message(F.text.lower().contains("feedback"))
async def feedback_handler(message: types.Message):
    await message.answer("Feedback")


@user_private_router.message(Command("shipping"))
@user_private_router.message(
    (F.text.lower().contains("shipping methods"))
    | (F.text.lower() == "shipping info")
)
async def shipping_handler(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Shipping methods:"),
            "Pickup from the store",
            "Delivery to the door",
            "Post office delivery",
            marker="• ",
        ),
        as_marked_section(
            Bold("Contact us and make sure we can deliver to your address"),
            "Our delivery team phone number: +123456789",
        ),
        sep="\n----------------------------\n",
    )
    await message.answer(text.as_html())
