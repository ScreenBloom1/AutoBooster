from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1).add(
    KeyboardButton("🌟Мои темы"),
    KeyboardButton("ℹ️Информация")
)

admin = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    KeyboardButton("📊Статистика"),
    KeyboardButton("💬Рассылка"),
    KeyboardButton("🔃Выгру.дб"))