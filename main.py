## Этап 2. Переменные окружения, логирование и маршрутизация

# Дополнительный гайд по aiogram3 https://mastergroosha.github.io/aiogram-3-guide/
# Документация по aiogram3 https://docs.aiogram.dev/en/latest/
# Ссылка на форум aiogram в тг: https://t.me/aiogram

# 0. Установить зависимости
# pip install aiogram
# pip install python-dotenv

# 1. Импорт
import logging  # чтобы отследить состояние бота, используем логи
import asyncio  # асинхронный ввод-вывод
from aiogram import Bot, Dispatcher, types, filters  # класс бота и диспетчера
from config import TOKEN
from handlers import register_message_handler, commands_for_bot, check_new_files
from db import async_create_table
from threading import Thread

def loop_in_thread(loop):
    print('loop')
    asyncio.set_event_loop(loop)
    asyncio.run(check_new_files(TOKEN))

async def on_startup(dp):
    print('init')
    loop = asyncio.get_event_loop()
    t = Thread(target=loop_in_thread, args=(loop,))
    t.start()
    
async def main() -> None:
    """polling-запуск проекта"""

    # Установить общий уровень логирования
    logging.basicConfig(level=logging.DEBUG)

    # Экзампляры бота и диспетчера
    bot = Bot(TOKEN)
    dp = Dispatcher()
    
    await on_startup(dp)
    # Функция для вызова обработчиков
    await register_message_handler(dp)

    # Загрузка команд
    await bot.set_my_commands(commands=commands_for_bot)

    # polling-запуск
    await dp.start_polling(bot)


# 5. Запуск
if __name__ == "__main__":
    try:
        asyncio.run(async_create_table())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("GoodBye!")