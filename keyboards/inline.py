from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_btns(
    *,
    buttons: dict[str],
    sizes: tuple[int] = (2,),
):
    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()


def get_url_buttons(
    *,
    buttons: dict[str, str],
    sizes: tuple[int] = (2,),
):
    keyboard = InlineKeyboardBuilder()

    for text, url in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))
    return keyboard.adjust(*sizes).as_markup()


def get_inlineMix_btns(
    *,
    buttons: dict[str, str],
    sizes: tuple[int] = (2,),
):
    """
    Creates an inline keyboard with a mix of URL and callback buttons.

    The function takes a dictionary where each key-value pair represents the
    text and a URL/callback data for a button. If the value contains "://",
    it is treated as a URL; otherwise, it's treated as callback data.

    Args:
        buttons: A dictionary with the button text as keys and URLs or
                 callback data as values.
        sizes: A tuple representing row sizes of the keyboard.

    Returns:
        InlineKeyboardMarkup: The constructed inline
        keyboard markup ready for use.
    """
    keyboard = InlineKeyboardBuilder()

    for text, value in buttons.items():
        if "://" in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))
    return keyboard.adjust(*sizes).as_markup()
