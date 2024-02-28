from aiogram.types import BotCommand

# if not dp.resolve_user_update_types()
ALLOWED = ["message", "edited_message", "callback_query"]

PRIVATE_MENU = [
    BotCommand(command="menu", description="Open menu"),
    BotCommand(command="about", description="About"),
    BotCommand(command="payment", description="Payment methods"),
    BotCommand(command="shipping", description="Shipping methods"),
    BotCommand(command="feedback", description="Feedback"),
]


# text fields
ABOUT = (
    "Welcome to our Gem Store! 🛍️ \nWe're"
    "your go-to destination for unique finds, "
    "rare items, and second-hand treasures. "
    "As a locally-owned shop run by a passionate "
    "couple, we curate a diverse selection of "
    "goods that are sure to spark joy and add "
    "character to your life. From vintage gems "
    "to one-of-a-kind pieces, we're dedicated "
    "to bringing you quality products with a personal "
    "touch. Explore our collections and let us help "
    "you discover something special today! "
)
