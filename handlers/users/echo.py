from unittest import case
from handlers.users import misc as ms
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import ik,kb
from loader import dp
from data import text
from data import config as cfg
from handlers.users import lt
from states import st


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if str(message.from_user.id) in cfg.ADMINS:
        match message.text:
            case "Админ":
                await message.answer("Админ меню:", reply_markup=kb.admin)
            case "📊Статистика":
                await message.answer(lt.admin_stat(), reply_markup=kb.admin)
            case "💬Рассылка":
                await message.answer("Пришлите мне сообщение, которое будет разослано пользователям")
                await st.UserState.sender.set()
                return
            case "🔃Выгру.дб":
                document = ms.get_ids_files()
                await message.answer_document(document=document,
                                              caption="Файл с ID пользователей")
                return

    match message.text:
        case "🌟Мои темы":
            await message.answer("<b>Ваши темы:</b>",reply_markup=ik.topic(message.from_user.id))
        case "ℹ️Информация":
            await message.answer(text.info,reply_markup=kb.main)