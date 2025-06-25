from aiogram import executor
from loader import dp  # твой диспетчер
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify
from handlers.users.up_topic import auto_bump_loop
import asyncio

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    asyncio.create_task(auto_bump_loop())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


