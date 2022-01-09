from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.client_keyboards import *
from async_functions.functions import *


async def start_command(message: types.Message) -> None:
    """
    Стартовая функция приветствия
    :param message: сообщение от пользователя
    :return: ответное приветствие
    """
    await message.answer('<i><b>Добро пожаловать в бота для проверки своих оценок'
                         '\nНажмите "Войти", чтобы выполнить вход в ориокс</b></i>',
                         reply_markup=start_keyboard()
                         )


class FSMForm(StatesGroup):
    """
    Форма ввода логина и пароля
    """
    username = State()
    password = State()


async def login_command(message: types.Message) -> None:
    """
    Функция, запращивающая ввод пользователем логина
    :param message: сообщение "Войти"
    :return: ответ с просьбой ввести логин
    """
    await FSMForm.username.set()
    await message.answer("Введите номер студенческого", reply_markup=types.ReplyKeyboardRemove())


async def enter_username(message: types.Message, state: FSMContext) -> None:
    """
    Функция, обрабатывающая ввод логина от ориокса
    :param state: состояние формы
    :param message: сообщение, содержащее логин
    :return: ответ с просьбой ввести пароль
    """
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMForm.next()
    await message.answer("Введите пароль")


async def enter_password(message: types.Message, state: FSMContext) -> None:
    """
        Функция, обрабатывающая ввод пароля. Сохраняет все данные из storage в базу
        :param state: состояние формы
        :param message: сообщение, содержащее пароль
        :return: ответ об успешном получении данных
        """
    async with state.proxy() as data:
        data['password'] = message.text
    async with state.proxy() as data:
        user_data = dict()
        user_data["username"] = data.get("username")
        user_data["password"] = data.get("password")
        user_data["telegram_username"] = message.from_user.username
        res = await register_user(user_data)
        await message.answer(res.get("msg"), reply_markup=main_keyboard())
    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Функция, обрабатывающпя отмену введения данных. Выполняет сброс машины состояния
    :param message: сообщение от пользователя
    :param state: текущее состояние FSM
    :return: сброс настроек не выполняется, если состояние пусто
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Действия отменены", reply_markup=start_keyboard())


async def get_marks_handler(message: types.Message) -> None:
    """
    Функция, обрабатывающая запрос на выдачу оценок. Запускает функцию, которая отправляет запрос к API
    :param message: сообщение от пользователя
    :return: возвращает сообщение с оценками на текущую неделю
    """
    await message.answer("Пожалуйста подождите")
    res = await get_marks(message.from_user.username)
    if res.get("msg"):
        await message.answer(res.get("msg"), reply_markup=main_keyboard())
    else:
        res = res.get("get_json_marks")
        marks = ''
        for k, v in res.items():
            marks += f"{v['subject']}: {v['mark']}\n"  # собираю в один тест через f - строки
        await message.answer(marks, reply_markup=main_keyboard())


async def start_checking(message: types.Message) -> None:
    """
    Функция, запускающая ежечасную проверку оценок
    :param message: сообщение от пользователя
    """
    loop = asyncio.get_event_loop()
    loop.create_task(check_updates_by_username(message.from_user.username, message))


def register_client_handlers(dp: Dispatcher) -> None:
    """
    Функция, регистрирующая все обработчики для пользовательских запросов
    :param dp: объект Dispatcher
    """
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, lambda message: message.text.lower() == "отмена", state="*")
    dp.register_message_handler(login_command, lambda message: message.text == "Войти", state=None)
    dp.register_message_handler(get_marks_handler, lambda message: message.text == "Получить оценки", state=None)
    dp.register_message_handler(start_checking, lambda message: message.text == "Запустить ежечасную проверку оценок",
                                state=None)
    dp.register_message_handler(enter_username, state=FSMForm.username)
    dp.register_message_handler(enter_password, state=FSMForm.password)
