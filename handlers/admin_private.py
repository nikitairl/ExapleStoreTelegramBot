from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import crud_add_product
from exceptions import ADD_PRODUCT_ERROR
from filters.chats import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Add product",
    "Change product",
    "Delete product",
    "Starring at product",
    placeholder="What do you want?",
    sizes=(2, 1, 1),
)


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("What do you want?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Starring at product")
async def starring_at_product(message: types.Message):
    await message.answer("OK, here is the list of products")


@admin_router.message(F.text == "Change product")
async def change_product(message: types.Message):
    await message.answer("OK, here is the list of products:")


@admin_router.message(F.text == "Delete product")
async def delete_product(message: types.Message):
    await message.answer("Pick the product(s) you want to delete")


# FSM ######### FSM ######### FSM ######### FSM ######### FSM ######### FSM #
class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Please enter the name:',
        'AddProduct:description': 'Please enter the description:',
        'AddProduct:price': 'Please enter the price:',
        'AddProduct:image': 'Please send me the image...',
    }


@admin_router.message(StateFilter(None), F.text == "Add product")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Enter the name", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command("cancel"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Cancelled", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'), Command("back"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "back")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('There is no previous state')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"OK, previous state: \n {AddProduct.texts[previous.state]}"
            )
            return
        previous = step


@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if len(message.text) >= 100:
        await message.answer(
            "Product name is too long(>100). \n Please enter the name again"
        )
        return

    await state.update_data(name=message.text)
    await message.answer("Enter the description")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_name_bad_data(message: types.Message, state: FSMContext):
    await message.answer(
        "Wrong data? Fix and repeat"
    )


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Enter the price")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.description)
async def add_description_bad_data(message: types.Message, state: FSMContext):
    await message.answer(
        "Wrong data? Fix and repeat"
    )


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    try:
        float(message.text)
    except ValueError:
        await message.answer("Wrong data. Please enter the price again")
        return

    await state.update_data(price=message.text)
    await message.answer("Upload the image")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.price)
async def add_price_bad_data(message: types.Message, state: FSMContext):
    await message.answer("Wrong data? Fix and repeat")


@admin_router.message(AddProduct.image, F.photo)
async def add_image(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Success! Product added", reply_markup=ADMIN_KB)
    data = await state.get_data()
    try:
        await crud_add_product(session, data)
    except ADD_PRODUCT_ERROR:
        await session.rollback()
        await message.answer(f"Error: {ADD_PRODUCT_ERROR}")
    await message.answer(str(data))
    await state.clear()


@admin_router.message(AddProduct.image)
async def add_image_wrong_data(message: types.Message, state: FSMContext):
    await message.answer("Wrong data? Fix and repeat")
