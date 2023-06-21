from aiogram.utils import executor

from bot.bot_init import dp, startup, shutdown

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)