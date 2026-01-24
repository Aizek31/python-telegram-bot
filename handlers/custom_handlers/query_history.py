from telebot.types import Message
from loader import bot
from states.history import HistoryState
from datetime import date
import re
from database.orm_history import get_history_by_date, get_database
from utils.filters_films_custom import caption_for_history


@bot.message_handler(commands=["history"])
def ask_data_search(message) -> None:
    """
    Обработчик команды /history/
    Устанавливает состояние ожидания ввода даты за который производиться поиск.

    :param message: объект сообщения Telegram от пользователя.
    :return: None
    """

    bot.set_state(message.from_user.id, HistoryState.date_search, message.chat.id)
    bot.send_message(
        message.chat.id,
        "🌟 Добро пожаловать в историю поиска! 🌟\n📅 Пожалуйста, введите дату, за которую хотите посмотреть историю поиска! 📅\n\n😊 Например: 2026-01-19 😊",
    )


@bot.message_handler(state=HistoryState.date_search)
def query_output(message: Message) -> None:
    text = message.text
    # Разделяем и преобразуем в дату
    # Сделать функцию
    year, month, day = map(int, re.split("[,-.]", text))
    date_obj = date(year, month, day)

    db = get_database()
    films = get_history_by_date(date_obj, db)

    for film in films:
        print(film)
        caption = caption_for_history(film)
        bot.send_photo(
            chat_id=message.chat.id,
            photo=film["poster_url"],
            caption=caption,
            parse_mode="Markdown",
        )
