from telebot.types import Message
from loader import bot
import os


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, "afisha.jpg")
    # ✅ Правильно: используем with для авто-закрытия
    with open(file_path, "rb") as photo:
        caption = (
            "<b>Что умеет этот бот?</b>\n\n"
            "Привет! 🎬 Я твой персональный помощник в мире кино. 😎\n\n"
            "Хотите найти идеальный фильм для любого настроения или жанра?\n"
            "Тогда жмите кнопку «/help»."
        )
        bot.send_photo(message.chat.id, photo=photo, caption=caption, parse_mode="HTML")
