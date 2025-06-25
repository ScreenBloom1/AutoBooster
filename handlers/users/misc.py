from utils.db_api import database as db
from datetime import datetime
import asyncio
from loader import bot
from keyboards import ik


def get_time_for_last_topic(data):
    # Проверяем, если время равно 0
    if data['time'] == 0:
        return "Тема пока что не может быть поднята."

    # Если время представлено как временная метка (int или float)
    if isinstance(data['time'], (int, float)):
        time_recorded = datetime.fromtimestamp(data['time'])
    else:
        # Если время представлено как строка
        time_str = str(data['time'])
        try:
            time_recorded = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise ValueError(
                f"Некорректный формат времени: {time_str}. Ожидается формат 'YYYY-MM-DD HH:MM:SS' или временная метка") from e

    # Вычисляем разницу между текущим временем и временем записи
    current_time = datetime.now()
    time_difference = current_time - time_recorded
    total_seconds = int(time_difference.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours} часа {minutes} минут"

def get_ids_files():
    ids = db.get_user_ids()
    text = ""
    file = open("db_ids.txt",'w')
    for id in ids:
        text+=f"{id}\n"
    file.write(text)
    file.close()
    return open("db_ids.txt",'rb')

def get_count_of_user(days,user_datas):
    counter = 0
    for data in user_datas:
        date = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - date).days < days:
            counter+=1
    return counter


async def sender(message_id,from_chat_id,name,url):
    if name == "0" or url == "0":
        ids = db.get_user_ids()
        i = 0
        for user_id in ids:
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id,
                                       message_id=message_id)
                i+=1
            except:
                pass
            await asyncio.sleep(0.2)
        await bot.send_message(chat_id=from_chat_id,text=f"Рассылка дошла до {i} пользователей")
    else:
        ids = db.get_user_ids()
        i = 0
        for user_id in ids:
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id,
                                       message_id=message_id,reply_markup=ik.create_sender_mrkp(name,url))
                i += 1
            except:
                pass
            await asyncio.sleep(0.2)
        await bot.send_message(chat_id=from_chat_id, text=f"Рассылка дошла до {i} пользователей")