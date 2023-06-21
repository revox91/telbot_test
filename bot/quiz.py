import json

from loguru import logger
from pydantic import BaseModel


class Question(BaseModel):
    id: int = 0
    Q: str = None
    A_1: str = None
    A_2: str = None
    A_3: str = None
    A_4: str = None
    CORRECT: str = ""


class StartQ(BaseModel):
    id: int = 0
    Q: str = "Укажите Ваш пол"
    A_1: str = "Мужской"
    A_2: str = "Женский"


class Q(Question):
    id: int = "1"
    Q: str = "Что такое Атихифобия?"
    A_1: str = "Страх совершить ошибку"
    A_2: str = "Боязнь пауков"
    A_3: str = "Страх перед едой"
    A_4: str = "Страх приёма лекарственных средств"
    CORRECT: str = A_1


class Q1(Question):
    id: int = "2"
    Q: str = 'Сколько времени продлился полёт первого искусственного спутника Земли “Спутник — 1”'
    A_1: str = "1 месяц"
    A_2: str = "3 месяца"
    A_3: str = "28 дней"
    A_4: str = "8 дней"
    CORRECT: str = A_2


class Q2(Question):
    id: int = "3"
    Q: str = "Какое из этих слов не является методом обучения?"
    A_1: str = "Шедоуинг"
    A_2: str = "Баддинг"
    A_3: str = "Коучинг"
    A_4: str = "Флоатинг"
    CORRECT: str = A_4


class Q3(Question):
    id: int = "4"
    Q: str = "Какой срок годности ГОСТ предписывал советскому мороженому?"
    A_1: str = "14 дней"
    A_2: str = "Месяц"
    A_3: str = "5 дней"
    A_4: str = "Неделя"
    CORRECT: str = A_4


class Q4(Question):
    id: int = "5"
    Q: str = "Что не является вакциной от коронавируса?"
    A_1: str = "Новавакс"
    A_2: str = "Спутник V"
    A_3: str = "Джонсон и Джонсон"
    A_4: str = "Сенека"
    CORRECT: str = A_3


class Q5(Question):
    id: int = "6"
    Q: str = "Когда отмечается день российской науки?"
    A_1: str = "08.03"
    A_2: str = "08.02"
    A_3: str = "14.04"
    A_4: str = "08.09"
    CORRECT: str = A_2


START_QUIZ = StartQ()
ALL_Q = [Q(), Q1(), Q2(), Q3(), Q4(), Q5()]
QUIZ_1_IDS = ["1", "2", "3"]
QUIZ_2_IDS = ["4", "5", "6"]
QUIZ_ANSWERS = {q.id: q.CORRECT for q in ALL_Q}
ALL_QUESTIONS_DICT = dict(zip(["1", "2", "3", "4", "5", "6"], ALL_Q))


class QuizController:
    @staticmethod
    async def prepare_quiz_set_for_user(answer: int) -> dict:
        if answer == 0:
            return dict.fromkeys(QUIZ_1_IDS, None)
        return dict.fromkeys(QUIZ_2_IDS, None)

    @staticmethod
    async def get_user_answers(cached_answers: dict, with_results: bool = False):
        res = []
        i = 1
        for k, v in cached_answers.items():
            logger.warning(f'{k,v}')
            question_as_dict = ALL_QUESTIONS_DICT[k].dict()
            user_answer = question_as_dict[v]
            result_str = f"""{i}) Вопрос: "{question_as_dict['Q']}"\nВаш ответ: "{user_answer}" \n"""
            if with_results:
                result_str += f"""Правильный ответ: "{question_as_dict["CORRECT"]}" \n\n"""
            res.append(result_str)
            i += 1
        return " ".join(res)

    @staticmethod
    async def result_json(cached_answers: dict):
        return json.dumps(cached_answers)

    @staticmethod
    async def get_results(cached_answers: dict):
        res = []
        i = 1
        for k, v in cached_answers.items():
            question_as_dict = ALL_QUESTIONS_DICT[k].dict()
            user_answer = question_as_dict[v]
            res.append(f"""{i}) Вопрос: "{question_as_dict['Q']}"\n Ваш ответ: "{user_answer}" \n\n""")
            i += 1
        return " ".join(res)

    @staticmethod
    async def get_next_question(cached_data: dict, user_id: str):
        next_q = None
        for k, v in cached_data[user_id].items():
            if v is None:
                next_q = ALL_QUESTIONS_DICT[k]
                break
        return next_q

    @staticmethod
    async def get_question(question_id: str):
        return ALL_QUESTIONS_DICT[question_id]