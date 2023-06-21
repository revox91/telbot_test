from aiogram import Bot, Dispatcher
from loguru import logger
from bot.config import CONFIG


bot = Bot(CONFIG.BOT_TOKEN)
dp = Dispatcher(bot)


async def startup(dp: Dispatcher):
    logger.info("bot started")


async def shutdown(dp: Dispatcher):
    logger.info("bot finished")
