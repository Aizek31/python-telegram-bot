from telebot.types import Message
from loader import bot


# для вывода приветственного сообщения и картинки
@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    # путь для картинки нужно будет переписать
    photo = open(
        "D:/Project_Python/python_basic_diploma/handlers/custom_handlers/afisha.jpg",
        "rb",
    )
    caption = (
        "<b>Что умеет этот бот?</b>\n\n"
        "Привет! 🎬 Я твой персональный помощник в мире кино. 😎\n\n"
        "Хотите найти идеальный фильм для любого настроения или жанра?\n"
        "Тогда жмите кнопку «/help»."
    )

    bot.send_photo(message.chat.id, photo=photo, caption=caption, parse_mode="HTML")
