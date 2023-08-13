from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from afisha_bot.state.state import STATE
from afisha_bot.repository import repository


def get_state(user_id: int) -> dict:
    return STATE[user_id]


def set_state(user_id: int, data: dict) -> None:
    STATE[user_id] = data


def get_category() -> dict:
    data = repository.get_category()
    res = {}

    for item in data:
        res[f"btn{item[0]}"] = item[1]
    return res


def get_user_category(user_id: int) -> list:
    return repository.get_user_category(user_id)



def set_user(user_id: int, nickname: str, username: str, category_ids: list) -> bool:
    return repository.set_user(user_id, username, nickname, category_ids)


def update_category_ids(user_id: int, category_ids: list) -> None:
    repository.update_category_ids(user_id, category_ids)


def create_keyboard_category(user_id: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    temp_data = []

    for key, value in STATE[user_id].items():
        if len(temp_data) < 2:
            temp_data.append(
                types.InlineKeyboardButton(text=value, callback_data=key))
        else:
            builder.row(*temp_data)
            temp_data.clear()
            temp_data.append(
                types.InlineKeyboardButton(text=value, callback_data=key))
    builder.row(
        types.InlineKeyboardButton(text="Готово!", callback_data="done"))

    return builder
