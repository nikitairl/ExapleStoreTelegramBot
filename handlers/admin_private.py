from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import (
    crud_add_product,
    crud_delete_product,
    crud_get_product,
    crud_get_products,
    crud_update_product,
)
from filters.chats import ChatTypeFilter, IsAdmin
from keyboards.inline import get_inlineMix_btns
from keyboards.reply import get_keyboard
from utils.exceptions import ADD_PRODUCT_ERROR

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Add product",
    "Products",
    placeholder="What do you want?",
    sizes=(2,),
)


class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    changing_product = None

    texts = {
        "AddProduct:name": "Please enter the name:",
        "AddProduct:description": "Please enter the description:",
        "AddProduct:price": "Please enter the price:",
        "AddProduct:image": "Please send me the image...",
    }


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("What do you want?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Products")
async def starring_at_product(message: types.Message, session=AsyncSession):
    await message.answer("OK, here is the list of products if not empty:")
    for product in await crud_get_products(session):
        await message.answer_photo(
            product.image,
            caption=(
                f"Name: {product.name}\nDescription: "
                f"{product.description}\nPrice: {round(product.price, 2)}"
            ),
            reply_markup=get_inlineMix_btns(
                buttons={
                    "Edit": f"edit_{product.id}",
                    "Delete": f"delete_{product.id}",
                }
            ),
        )


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    try:
        await crud_delete_product(session, int(product_id))
    except Exception:
        await callback.message.answer("Delete error, try again")
    await callback.answer("Product deleted")
    await callback.message.answer("OK, product deleted")


@admin_router.callback_query(StateFilter(None), F.data.startswith("edit_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]
    changing_product = await crud_get_product(session, int(product_id))
    print(changing_product)

    AddProduct.changing_product = changing_product
    await callback.answer()
    await callback.message.answer(
        "Enter the name",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(AddProduct.name)


# FSM ######### FSM ######### FSM ######### FSM ######### FSM ######### FSM #


@admin_router.message(StateFilter(None), F.text == "Add product")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Enter the name", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter("*"), Command("cancel"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Cancelled", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter("*"), Command("back"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "back")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer("There is no previous state")
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
    if message.text == "-":
        await state.update_data(name=AddProduct.changing_product.name)
    else:
        if len(message.text) >= 100:
            await message.answer(
                "Product name is too long(>100). \n Enter the name again"
            )
            return

        await state.update_data(name=message.text)
    await message.answer("Enter the description")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_name_bad_data(message: types.Message, state: FSMContext):
    await message.answer("Wrong data? Fix and repeat")


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    if message.text == "-":
        await state.update_data(
            description=AddProduct.changing_product.description
        )
    else:
        await state.update_data(description=message.text)
    await message.answer("Enter the price")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.description)
async def add_description_bad_data(message: types.Message, state: FSMContext):
    await message.answer("Wrong data? Fix and repeat")


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "-":
        await state.update_data(price=AddProduct.changing_product.price)
    else:
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


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "-"))
async def add_image(
    message: types.Message, state: FSMContext, session: AsyncSession
):
    if message.text and message.text == "-":
        await state.update_data(image=AddProduct.changing_product.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.changing_product:
            await crud_update_product(
                session, AddProduct.changing_product.id, data
            )
        else:
            await crud_add_product(session, data)
        await message.answer("Success! Product added", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}",
            reply_markup=ADMIN_KB,
        )
    AddProduct.changing_product = None


@admin_router.message(AddProduct.image)
async def add_image_wrong_data(message: types.Message, state: FSMContext):
    await message.answer("Wrong data? Fix and repeat")
