import asyncio
import aiohttp
from utils.db_api import database as db
from loader import bot
from data import config as cfg
from datetime import datetime


async def bump_thread(token: str, thread_id: int):
    url = f"https://prod-api.lolz.live/threads/{thread_id}/bump"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                if response.status == 429:
                    # Если сервер возвращает 429, ждём 60 секунд и повторяем запрос
                    await asyncio.sleep(60)
                    return await bump_thread(token, thread_id)
                return response.status
    except Exception as e:
        return 450

async def auto_bump_loop():
    while True:
        topics = db.get_all_topic_rows()

        for topic in topics:
            thread_id = topic.get("thread_id")
            user_id = topic.get('id_user')
            token = db.get_user(user_id)['token']
            id_topic = topic.get('id')
            username = db.get_user(user_id)['username']

            if not token or not thread_id:
                continue

            status_code = await bump_thread(token, thread_id)
            if status_code == 200:
                await bot.send_message(chat_id=user_id, text=f"✔️Тема https://lolz.live/threads/{thread_id}/ только что была поднята!")
                await bot.send_message(chat_id=cfg.CHAT_ID, text=f"✔️Тема <b>{thread_id}</b> usera @{username} только что была поднята!")
                db.update_topic_table(id_topic, 'time', str(datetime.now())[:19])
            elif status_code == 401:
                await bot.send_message(chat_id=cfg.CHAT_ID,text=f"Тема {thread_id} usera @{username} не может быть поднята и удаляется, невалид токен.")
                db.delete_topic(id_topic)
            elif status_code == 450:
                await bot.send_message(chat_id=cfg.CHAT_ID, text=f"Ошибка по теме {thread_id} usera @{username} и удалена сразу")
                db.delete_topic(id_topic)
            elif status_code == 403:
                pass
            await asyncio.sleep(10)
        await asyncio.sleep(60)

