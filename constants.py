from aiogram.types import BotCommand

ALLOWED = ["message", "edited_message"]
PRIVATE_MENU = [
    BotCommand(command="menu", description="Open menu"),
    BotCommand(command="about", description="About"),
    BotCommand(command="payment", description="Payment methods"),
    BotCommand(command="shipping", description="Shipping methods"),
    BotCommand(command="feedback", description="Feedback"),
]
