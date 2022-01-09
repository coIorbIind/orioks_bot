from aiogram.utils.exceptions import BotBlocked
from aiogram import types
from aiogram.dispatcher import Dispatcher


# @dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked) -> bool:
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


def register_exceptions_handler(dp: Dispatcher) -> None:
    dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)
