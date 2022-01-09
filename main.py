from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


import os
from sys import exit


from handlers import client, other, exceptions
from async_functions.functions import get_users_for_check, start_loop


async def on_startup(_) -> None:
    """
    Функция, которая срабатывает при запуске бота. Она получает пользователей, у которых включена автопроверка оценок и
    запускает ее для каждого
    :param _:
    """
    # result = await get_users_for_check()
    # if result.get("msg"):
    #     print(result.get("msg"))
    # users = result.get("users")
    # for user in users:
    #     await start_loop(username=user.get("username"), user_id=user.get("username"), bot=bot)
    print("Success")


if __name__ == "__main__":
    """
    Создается объект бота, диспатчера и хранилища данных.
    Регистрация обработчиков пользователесного ввода.
    Запуск long polling'а
    """
    # Создание хранилища данных
    storage = MemoryStorage()
    # Создание бота
    bot_token = os.getenv("TOKEN")
    if not bot_token:
        exit("[ERROR] No token provided")

    bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)

    # Регистрания handlers
    client.register_client_handlers(dp)
    exceptions.register_exceptions_handler(dp)
    other.register_other_handlers(dp)

    # Запуск поллинга
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
