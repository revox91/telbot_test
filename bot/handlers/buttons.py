from typing import Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from bot.quiz import Question, StartQ

main_menu_button = [InlineKeyboardButton(text="Начать опрос", callback_data="start_quiz")]

submit_button = [InlineKeyboardButton(text="Подтвердить", callback_data="submit")]

show_answers_buttons = [[InlineKeyboardButton(text="Посмотреть ответы", callback_data="show_answers")],
                        submit_button]

edit_buttons = [[InlineKeyboardButton(text="Изменить ответ", callback_data="edit")],
                submit_button]

result_json_buttons = [[InlineKeyboardButton(text="Показать ответы в виде JSON", callback_data="json")],
                       main_menu_button]

menu_kbd = InlineKeyboardMarkup(inline_keyboard=[main_menu_button])
show_answers_kbd = InlineKeyboardMarkup(inline_keyboard=show_answers_buttons)
edit_kbd = InlineKeyboardMarkup(inline_keyboard=edit_buttons)
result_json_kbd = InlineKeyboardMarkup(inline_keyboard=result_json_buttons)


class ButtonsController:
    @classmethod
    async def alias(cls, q_id: int, key: str, fork: bool = False):
        if fork:
            return f"{q_id}-{key}-F"
        return f"{q_id}-{key}"

    @classmethod
    async def generate_buttons(cls, q: Union[Question, StartQ]):
        data = q.dict()
        logger.debug(data)
        answer_buttons = [
            [InlineKeyboardButton(
                text=data[k],
                callback_data=await cls.alias(q.id, k) if q.id != 0 else await cls.alias(q.id, k, fork=True))]
            for k in data.keys() if "A" in k
        ]
        return InlineKeyboardMarkup(inline_keyboard=answer_buttons)

    @classmethod
    async def generate_edit_buttons(cls, question_ids: list):
        edit = [
            [InlineKeyboardButton(text=f"Изменить ответ на вопрос {i+1}", callback_data=f"edit-{q_id}")]
            for i, q_id in enumerate(question_ids)
        ]
        edit.append(submit_button)
        return InlineKeyboardMarkup(inline_keyboard=edit)


