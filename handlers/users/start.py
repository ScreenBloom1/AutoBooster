from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api import database as db
from loader import dp
from keyboards import ik,kb


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    db.create_user(message.from_user.id,message.from_user.username)
    await message.answer(f"<b>Привет!</b> Я бот для автоматического поднятия тем на lolz.live. Просто заполняй нужные данные, и я сделаю всё остальное! 🚀",reply_markup=kb.main)
