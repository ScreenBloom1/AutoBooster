from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from handlers.users import misc as ms
from loader import dp
from keyboards import ik,kb
from aiogram.dispatcher import FSMContext
from states import st
from handlers.users import lt
from utils.db_api import database as db


@dp.callback_query_handler(state="*")
async def main(call: types.CallbackQuery, state: FSMContext):
    params = call.data.split("-")
    match params[0]:
        case "add_topic":
            await call.message.delete()
            if db.get_user(call.from_user.id)['token'] == "0":
                await call.message.answer("Для добавления темы, в первую очередь необходимо отправить ваш <b>TOKEN</b>. Вы можете получить его по ссылке: https://lolz.live/account/api",reply_markup=ik.off_state)
                await st.UserState.add_token.set()
            else:
                await call.message.answer("Теперь отправьте <b>ссылку</b> на тему, которую нужно поднимать. Пример: <code>https://lolz.live/threads/346456/</code>",reply_markup=ik.off_state)
                await st.UserState.add_id_2.set()


        case "topic":
            id = params[1]
            await call.message.edit_text(text=lt.profile_topic(id),reply_markup=ik.profile_topic(id))

        case "delete_topic":
            id = params[1]
            db.delete_topic(int(id))
            await call.message.delete()
            await call.message.answer("<b>Ваши темы:</b>",reply_markup=ik.topic(call.from_user.id))

        case "back_to_topic":
            await call.message.edit_text("<b>Ваши темы:</b>",reply_markup=ik.topic(call.from_user.id))

        case "off_state":
            await call.message.delete()
            await state.finish()
        case "send":
            await call.message.delete()
            message_id = int(params[1])
            data = await state.get_data()
            await state.finish()
            if len(data) != 0:
                name = data['name']
                url = data['url']
            else:
                name = "0"
                url = "0"
            from_chat_id = call.from_user.id
            await call.message.answer("Рассылка запущена")
            await ms.sender(message_id, from_chat_id, name, url)

        case 'add_button_to_send':
            message_id = int(params[1])
            await call.message.answer("Введите ссылку кнопки", reply_markup=ik.off_state)
            await st.UserState.add_btn_url.set()
            await state.update_data(message_id=message_id)