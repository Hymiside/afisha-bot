import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from afisha_bot.settings import Settings
from afisha_bot.service import service

settings = Settings()

bot = Bot(token=settings.bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    category = service.get_category()
    service.set_state(user_id, data=category)

    builder = service.create_keyboard_category(user_id)

    if service.set_user(user_id, message.from_user.username, message.from_user.first_name, []):
        await message.answer(
            f"*Привет, {message.from_user.first_name}*!"
            f"\n\nЭтот бот расскажет о самых крутых мероприятиях, проходящих в Перми."
            f"\n\n_Для начала выберите категории:_", reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)

    else:
        await message.answer("Подбираем для вас самые крутые мероприятия в Перми!")


@dp.callback_query(Text(startswith="btn"))
async def pick_category(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    button_id = callback.data

    st = service.get_state(user_id)

    if "✓" in st[button_id]:
        st[button_id] = st[button_id][2:]
    else:
        st[button_id] = f"✓ {st[button_id]}"

    service.set_state(user_id, st)
    builder = service.create_keyboard_category(user_id)

    await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(Text("done"))
async def done_pick_category(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    st = service.get_state(user_id)

    res = [int(key[3:]) for key, value in st.items() if "✓" in value]
    service.update_category_ids(user_id, res)

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Мои интересы"))

    await callback.message.answer(
        "*Отлично!*\n\nМы создали ваш профиль, теперь вам будут приходить "
        "уведомления о мероприятиях под ваши интересы.\n\nВы всегда можете отредактировать их, назав кнопку ниже.",
        reply_markup=builder.as_markup(resize_keyboard=True), parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

    data = service.get_last_mailings(res)
    if len(data) != 0:
        if len(data) > 5:
            data = data[:5]

        for i in data:
            builder_link = InlineKeyboardBuilder()
            builder_link.add(types.InlineKeyboardButton(text="Подробнее", url=i[7]))

            await bot.send_photo(chat_id=user_id, photo=i[6],
                                 caption=f"*{i[1]}*\n\n{i[2]}\n\n_Дата:_ {i[3]}\n\n_Стоимость:_ {i[4]}",
                                 parse_mode=ParseMode.MARKDOWN, reply_markup=builder_link.as_markup())


@dp.message(Text("Мои интересы"))
async def edit_category(message: types.Message):
    user_id = message.from_user.id
    data = service.get_user_category(user_id)

    msg_data = ", ".join(data)
    if not data:
        msg_data = "У вас пока нет выбранных интересов"

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Редактировать", callback_data="edit"))

    await message.answer(f"*Ваши интересы:*\n\n{msg_data}", reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)


@dp.callback_query(Text("edit"))
async def new_pick_category(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    category = service.get_category()
    service.set_state(user_id, data=category)

    builder = service.create_keyboard_category(user_id)
    await callback.message.answer("Выберите категории:", reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())