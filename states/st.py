from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp,bot
import re
from utils.db_api import database as db
from keyboards import ik


class UserState(StatesGroup):
    add_token = State()
    add_id = State()
    add_id_2 = State()
    sender = State()
    add_btn_url = State()
    add_btn_name = State()



@dp.message_handler(state=UserState.add_token)
async def get_token(message: types.Message, state: FSMContext):
    token = message.text
    await state.update_data(token=token)
    await message.answer("Теперь отправьте <b>ссылку</b> на тему, которую нужно поднимать. Пример: <code>https://lolz.live/threads/346456/</code>",reply_markup=ik.off_state)
    await UserState.add_id.set()


@dp.message_handler(state=UserState.add_id)
async def get_id(message: types.Message, state: FSMContext):
    match = re.search(r'https://lolz\.live/threads/(\d+)/', message.text.strip())
    if not match:
        await message.answer("❌ Неверный формат ссылки. Попробуйте снова.",reply_markup=ik.off_state)
        return
    thread_id = int(match.group(1))
    data = await state.get_data()
    token = data.get("token")
    db.create_table_topic(thread_id, message.from_user.id)
    db.update_userfield(message.from_user.id,'token',token)
    await message.answer(f"<b>Отлично</b>.\nТокен сохранён.\nID темы: <code>{thread_id}</code>\nТеперь тема будет автоматически подниматься. ✅")
    await state.finish()

@dp.message_handler(state=UserState.add_id_2)
async def get_id(message: types.Message, state: FSMContext):
    match = re.search(r'https://lolz\.live/threads/(\d+)/', message.text.strip())
    if not match:
        await message.answer("❌ Неверный формат ссылки. Попробуйте снова.",reply_markup=ik.off_state)
        return
    thread_id = int(match.group(1))
    db.create_table_topic(thread_id, message.from_user.id)
    await message.answer(f"<b>Отлично</b>.\nТокен сохранён.\nID темы: <code>{thread_id}</code>\nТеперь тема будет автоматически подниматься. ✅")
    await state.finish()

@dp.message_handler(state=UserState.sender,content_types=types.ContentType.ANY)
async def main(message: types.Message,state: FSMContext):
    msg_id = message.message_id
    await bot.copy_message(chat_id=message.from_user.id,from_chat_id=message.from_user.id,
                           message_id=msg_id)
    await message.answer("Рассылаем?",reply_markup=ik.send(msg_id))
    await state.finish()

@dp.message_handler(state=UserState.add_btn_url)
async def main(message: types.Message,state: FSMContext):
    url = message.text
    await state.update_data(url=url)
    await message.answer("Введите надпись на кнопке")
    await UserState.add_btn_name.set()

@dp.message_handler(state=UserState.add_btn_name)
async def main(message: types.Message,state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    data = await state.get_data()
    mrkp = ik.create_sender_mrkp(name,data['url'])
    message_to_send = await bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                           message_id=data['message_id'],reply_markup=mrkp)
    await message.answer('Рассылаем?',reply_markup=ik.send(message_to_send.message_id))