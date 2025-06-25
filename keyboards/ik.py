from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from utils.db_api import database as db


def topic(user_id):
    topics = db.get_topics_by_user_id(user_id)
    keyboard_buttons = []
    for topic in topics:
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"📌 Тема: {topic['thread_id']}",
                callback_data=f"topic-{topic['id']}"
            )
        ])
    keyboard_buttons.append([
        InlineKeyboardButton(
            text="➕ Добавить тему",
            callback_data="add_topic"
        )
    ])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard

def profile_topic(id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="< Назад",callback_data="back_to_topic"),
        InlineKeyboardButton(text="🗑Удалить",callback_data=f"delete_topic-{id}")
    )

def send(message_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="💬Разослать",callback_data=f'send-{message_id}'),
        InlineKeyboardButton(text="➕Добавить кнопку",callback_data=f'add_button_to_send-{message_id}'),
        InlineKeyboardButton(text="❌Отмена", callback_data='off_state')
    )


def create_sender_mrkp(name,url):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text=name,url=url)
    )

off_state = InlineKeyboardMarkup().add(InlineKeyboardButton(text="❌Отмена",callback_data='off_state'))

