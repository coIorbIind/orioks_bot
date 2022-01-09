import asyncio
from aiogram import types, Bot
import aiohttp

register_url = r"http://127.0.0.1:8000/api/create/"
marks_url = r"http://127.0.0.1:8000/api/marks/"
check_url = r"http://127.0.0.1:8000/api/check/"
users_url = r"http://127.0.0.1:8000/api/users/"


async def register_user(data: dict) -> dict:
    """
    Функция, выполняющая POST запрос к API, для регистрации пользователя в базе данных
    :param data: параметры пользователя: словарь, в котором содержатся следующие ключи и значения:
     username = номер студенческого
     password = пароль от Ориокса
     telegram_username = никнейм пользователя в telegram
    :return словарь с полученными данными: сообщение об успешном сохранении профиля или
        ошибке, произошедшей во время работы
    """
    async with aiohttp.ClientSession() as session:  # can be aiohttp.client_exceptions.ClientConnectorError
        async with session.post(url=register_url, data=data) as response:
            return await response.json()


async def get_marks(username: str) -> dict:
    """
    Функция, выполняющая запрос к API для получения оценок пользователя
    :param username: имя пользователя
    :return:
    """
    async with aiohttp.ClientSession() as session:
        url = f"{marks_url}?telegram_username={username}"
        async with session.get(url=url) as response:
            return await response.json()


async def check_updates_by_username(username: str, message: types.Message) -> None:
    """
    Функция, которая раз в час отправляет запрос к API и проверяет появление новых оценок у пользователя и отправляет
    ему сообщение, если такие появились. Для ответа использует сообщение от пользователя
    :param username: имя пользователя в telegram
    :param message: сообщение от пользователя, на которое будет следовать ответ
    """
    while True:
        async with aiohttp.ClientSession() as session:
            url = f"{check_url}?telegram_username={username}"
            async with session.get(url=url) as response:
                result = await response.json()
                if result.get("msg") in ["Профиль не найден", "Что-то пошло не так", "Изменения не найдены"]:
                    await message.answer(result.get("msg"))
                else:
                    marks = 'Новые оценки:\n'
                    for item in result.get("msg"):
                        marks += f"{item['subject']}: {item['mark']}\n"  # собираю в один тест через f - строки
                    await message.answer(marks)
        await asyncio.sleep(3600)


async def check_updates_by_id(username: str, user_id: str, bot: Bot) -> None:
    """
    Функция, которая раз в час отправляет запрос к API и проверяет появление новых оценок у пользователя и отправляет
    ему сообщение, если такие появились. Для ответа использует id пользователя и экземпляр класса Bot
    :param username: имя пользователя в telegram
    :param user_id: id telegram пользователя, которому нужно отправить сообщение
    :param bot: экземпляр класса Bot, который будет отправлять сообщения
    """
    while True:
        async with aiohttp.ClientSession() as session:
            url = f"{check_url}?telegram_username={username}"
            async with session.get(url=url) as response:
                result = await response.json()
                if result.get("msg") in ["Профиль не найден", "Что-то пошло не так", "Изменения не найдены"]:
                    await bot.send_message(chat_id=user_id, text=result.get("msg"))
                else:
                    marks = 'Новые оценки:\n'
                    for item in result.get("msg"):
                        marks += f"{item['subject']}: {item['mark']}\n"  # собираю в один тест через f - строки
                    await bot.send_message(chat_id=user_id, text=marks)
        await asyncio.sleep(3600)


async def start_loop(username: str, user_id: str, bot: Bot) -> None:
    """
    Функция, запускающая ежечасную проверку оценок
    :param username: имя пользователя в telegram
    :param user_id: id telegram пользователя, которому нужно отправить сообщение
    :param bot: экземпляр класса Bot, который будет отправлять сообщения
    """
    loop = asyncio.get_event_loop()
    loop.create_task(check_updates_by_id(username=username, user_id=user_id, bot=bot))


async def get_users_for_check() -> dict:
    """
    Функция, выполняющая запрос к API для получения всех пользователей, у которых включена автопроверка оценок
    :return: список всех пользователей, у которых включена автопроверка оценок
    """
    async with aiohttp.ClientSession() as session:
        url = users_url
        async with session.get(url=url) as response:
            return await response.json()
