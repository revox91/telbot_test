from aiogram import types
from aiogram.dispatcher.filters import Text
from loguru import logger

from bot.bot_init import dp
from bot.handlers.buttons import menu_kbd, ButtonsController, show_answers_kbd, result_json_kbd
from bot.quiz import START_QUIZ, QuizController
from bot.redis_db import CacheController


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    user = message.from_user.id
    logger.debug(f"user_id: {user}")
    await CacheController.restart(key=user)
    await message.answer(text="Добро пожаловать", reply_markup=menu_kbd)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text="Пожалуйста, продолжите опрос")


@dp.callback_query_handler(lambda c: c.data == 'start_quiz')
async def start_quiz(callback: types.CallbackQuery):
    user = callback.from_user.id
    logger.debug(user)
    await callback.message.edit_text(text=START_QUIZ.Q,
                                     reply_markup=await ButtonsController.generate_buttons(START_QUIZ))


@dp.callback_query_handler(Text(endswith="F"))
async def fork_question(callback: types.CallbackQuery):
    q_id, q_answer, fork = callback.data.split("-")
    q_set = await QuizController.prepare_quiz_set_for_user(q_answer)
    user_id = str(callback.from_user.id)
    cached = await CacheController.create_q_set(user_id=user_id, new_data=q_set)
    logger.info(cached)
    next_q = await QuizController.get_next_question(cached_data=cached, user_id=user_id)
    await callback.message.edit_text(text=next_q.Q,
                                     reply_markup=await ButtonsController.generate_buttons(next_q))


@dp.callback_query_handler(Text(contains="-A"))
async def answer(callback: types.CallbackQuery):
    q_id, q_answer = callback.data.split("-")
    user_id = str(callback.from_user.id)
    cached = await CacheController.update_answer(user_id=user_id, q_id=q_id, new_data=q_answer)
    logger.debug(cached)
    next_q = await QuizController.get_next_question(cached_data=cached, user_id=user_id)
    if next_q:
        await callback.message.edit_text(text=next_q.Q, reply_markup=await ButtonsController.generate_buttons(next_q))
    else:
        await callback.message.edit_text(text="Опрос окончен", reply_markup=show_answers_kbd)


@dp.callback_query_handler(lambda c: c.data == 'show_answers')
async def show_answers(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    cached = await CacheController.get(key=user_id)
    logger.debug(cached[user_id])
    res = await QuizController.get_user_answers(cached[user_id])
    await callback.message.edit_text(
        text=res,
        reply_markup=await ButtonsController.generate_edit_buttons(list(cached[user_id].keys()))
    )


@dp.callback_query_handler(Text(startswith="edit-"))
async def edit_answer(callback: types.CallbackQuery):
    q_id = callback.data.split("-")[-1]
    next_q = await QuizController.get_question(question_id=q_id)
    await callback.message.edit_text(text=next_q.Q, reply_markup=await ButtonsController.generate_buttons(next_q))


@dp.callback_query_handler(lambda c: c.data == 'submit')
async def submit(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    cached = await CacheController.get(key=user_id)
    logger.debug(cached[user_id])
    res = await QuizController.get_user_answers(cached[user_id], with_results=True)
    await callback.message.edit_text(text=res, reply_markup=result_json_kbd)


@dp.callback_query_handler(lambda c: c.data == 'json')
async def result_json(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    cached = await CacheController.get(key=user_id)
    await callback.message.edit_text(text=await QuizController.result_json(cached[user_id]), reply_markup=menu_kbd)

