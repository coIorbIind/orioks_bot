from aiogram import types
from aiogram.dispatcher import Dispatcher


async def echo_command(message: types.Message) -> None:
    await message.answer("Команда не распознана")


# @dp.message_handler(content_types=[types.ContentType.ANIMATION])
# async def echo_document(message: types.Message):
#     await message.answer_document(message.document.file_id)


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(echo_command)
    # dp.register_message_handler(echo_document, content_types=[types.ContentType.DOCUMENT])
