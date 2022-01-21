from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def start_keyboard() -> ReplyKeyboardMarkup:
    start_button = KeyboardButton('Войти')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button)
    return keyboard


def main_keyboard() -> ReplyKeyboardMarkup:
    check_button = KeyboardButton('Запустить ежечасную проверку оценок')
    get_button = KeyboardButton('Получить оценки')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(get_button)
    keyboard.add(check_button)
    return keyboard


def after_check_keyboard() -> ReplyKeyboardMarkup:
    check_button = KeyboardButton('Остановить ежечасную проверку оценок')
    get_button = KeyboardButton('Получить оценки')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(get_button)
    keyboard.add(check_button)
    return keyboard
# login_button = KeyboardButton('Войти')
# keyboard.add(login_button)
