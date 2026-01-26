from telebot.types import Message, InputMediaPhoto
from loader import bot
from datetime import date
import re
from database.orm_history import get_history_by_date, get_database
from utils.filters_films_custom import caption_for_history
from utils.pagination import send_character_page_history
from states.history import HistoryState
from logger_config import setup_logger


log = setup_logger(log_file=None, caller_file=__file__)


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

    try:
        text = message.text
        # Разделяем и преобразуем в дату
        # Сделать функцию
        year, month, day = map(int, re.split("[,-.]", text))
        date_obj = date(year, month, day)

        db = get_database()
        films = get_history_by_date(date_obj, db)
        print(films)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as history_films:
            history_films["catalog_movie"] = films

        first_movie = films[0]
        print(first_movie)
        caption = caption_for_history(first_movie)

        bot.send_photo(
            chat_id=message.chat.id,
            photo=first_movie["poster_url"],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=send_character_page_history(films),
        )
    except ValueError:
        bot.send_message(
            message.chat.id,
            "❌ Введите дату числом (например, 2025-09-15). Попробуйте ещё раз:",
        )

    except Exception as error:
        log.error(f"Error for user {message.from_user.id}: {error}")
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при поиске фильмов. Попробуйте позже или используйте /history",
        )


# Обработчик нажатий кнопок
@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.startswith("catalog_movie#")
)
def show_films(callback_query) -> None:
    bot.answer_callback_query(callback_query.id)
    page = int(callback_query.data.split("#")[1])

    # Берём сохраненные фильмы
    with bot.retrieve_data(
        callback_query.from_user.id, callback_query.message.chat.id
    ) as history_films:
        films = history_films["catalog_movie"]

    # Показываем фильм номер page (нумерация с 0)
    film = films[page - 1]
    paginator = send_character_page_history(films, page=page)
    caption = caption_for_history(film)
    media = InputMediaPhoto(
        media=film["poster_url"],
        caption=caption,  # ✅ Caption передаётся ЧЕРЕЗ InputMediaPhoto
        parse_mode="Markdown",
    )

    bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=media,
        reply_markup=paginator,
    )


# Сброс состояний
@bot.message_handler(commands=["cancel"])
def reset_search(message: Message) -> None:
    """
    Сбрасывает состояние пользователя и завершает текущий поиск.

    Очищает все сохраненные данные пользователя в FSM (Finite State Machine)
    и временные данные поиска. Отправляет уведомление о сбросе и напоминает
    о доступной команде для запуска нового поиска.

    :param message: Объект сообщения Telegram с командой /cancel
    :return: None
    """
    bot.reset_data(message.from_user.id, message.chat.id)
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "🔄 Поиск сброшен. Используйте /history")
