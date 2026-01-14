# TODO: тут будет код для поиска фильмов с низким бюджетом
from typing import Any
from telebot.types import Message

from keyboards.inline import gen_markup_genre
from states.user_information_budjet import UserState
from loader import bot
from api.api_kinopoisk_budget import (
    search_id_genre,
    search_movie,
    low_check_budget,
    big_check_budget,
)
from utils.filters_films_custom import filter_response, caption_for_rating_budget
from logger_config import setup_logger
from database.ORM import add_history


log = setup_logger(log_file=None, caller_file=__file__)
user_budget_type = {}


@bot.message_handler(commands=["low_budget_movie"])
def low_budget_movie(message: Message) -> None:
    """
    Обработчик команды /low_budget_movie.
    Устанавливает состояние ожидания ввода жанра фильма в FSM.

    :param message:
    :return: None
    """
    user_budget_type[message.from_user.id] = "low"
    bot.set_state(message.from_user.id, UserState.genre_cinema, message.chat.id)
    bot.send_message(
        message.chat.id,
        "🍿 Пожалуйста, выберите жанр фильма: 🎥",
        reply_markup=gen_markup_genre(),
    )


@bot.message_handler(commands=["high_budget_movie"])
def high_budget_movie(message: Message) -> None:
    """
    Обработчик команды /high_budget_movie.
    Устанавливает состояние ожидания ввода жанра фильма в FSM.

    :param message:
    :return: None
    """
    user_budget_type[message.from_user.id] = "high"
    bot.set_state(message.from_user.id, UserState.genre_cinema, message.chat.id)
    bot.send_message(
        message.chat.id,
        "🍿 Пожалуйста, выберите жанр фильма: 🎥",
        reply_markup=gen_markup_genre(),
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data, state=UserState.genre_cinema
)
def callback_handler(callback_query) -> None:
    """
    Сохряняет выбранный жанр и переходит к вводу года.
    """
    with bot.retrieve_data(
        callback_query.from_user.id, callback_query.message.chat.id
    ) as data:
        data["genre_cinema"] = callback_query.data

    bot.edit_message_reply_markup(
        callback_query.from_user.id,
        callback_query.message.message_id,
        reply_markup=None,
    )
    bot.send_message(
        callback_query.from_user.id,
        "Спасибо! 🎉 Записали выбранный вами жанр.\nТеперь введите год выпуска фильма: 📅",
    )
    bot.set_state(
        callback_query.from_user.id,
        UserState.year_cinema,
        callback_query.message.chat.id,
    )


# Финишный обработчик для бюджета
@bot.message_handler(state=UserState.year_cinema)
def finish_callback_handler(message: Message) -> None:
    """
    Обрабатывает год выпуска фильма, ищет низкобюджетные или высокобюджетные фильмы и отправляет результаты.

    :param message: объект сообщения Telegram от пользователя.
    :return: None.
    """

    budget_type = user_budget_type.get(message.from_user.id, "low")
    SUCCESS = False  # Флаг успешного завершения
    try:
        # Валидация года
        year = int(message.text)
        if not (1900 <= year <= 2026):
            bot.send_message(
                message.chat.id,
                "❌ Год должен быть в диапазоне от 1900 до 2026. Попробуйте еще раз:",
            )
            return

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if "genre_cinema" not in data:
                bot.send_message(
                    message.chat.id,
                    "❌ Ошибка: жанр не выбран. Введите /low_budget_movie",
                )
                return
            data["year"] = year
            target_genre = data["genre_cinema"]
            year_movie = data["year"]

        # достаёт id жанра
        id_genre = search_id_genre(target_genre)
        # ищет фильмы по id и году выпуска
        catalog_movie = search_movie(id_genre, year_movie)
        # отбирает фильмы по бюджету
        if budget_type == "high":
            bot.send_message(message.chat.id, "🔍 Ищем высокобюджетные фильмы...")
            big_budget = big_check_budget(catalog_movie)
            # вывод отфильтрованных фильмов
            filter_movie = filter_response(big_budget)
        else:
            bot.send_message(
                message.chat.id,
                "🔍 Ищем низкобюджетные фильмы...",
            )
            low_budget = low_check_budget(catalog_movie)
            # вывод отфильтрованных фильмов
            filter_movie = filter_response(low_budget)

        budget_text = "высокобюджетных" if budget_type == "high" else "низкобюджетных"
        if not filter_movie:

            bot.send_message(
                message.chat.id,
                f"😔 К сожалению, {budget_text} фильмы в этом жанре за указанный год не найдены.",
            )
            return

        bot.send_message(
            message.chat.id, f"✅ Найдено {len(filter_movie)} {budget_text} фильмов:"
        )

        # Запись найденных фильмов в базу данных
        add_history(filter_movie, message.from_user.id)
        # TODO: это можно переделать в функцию, где из жанров делается список
        for film in filter_movie:
            caption = caption_for_rating_budget(film)

            bot.send_photo(
                chat_id=message.chat.id,
                photo=film["posterUrlPreview"],
                caption=caption,
                parse_mode="Markdown",
            )
            SUCCESS = True  # ← Только при успехе

    except ValueError:
        bot.send_message(
            message.chat.id,
            "❌ Введите год числом (например, 2020). Попробуйте ещё раз:",
        )

    except Exception as error:
        log.error(f"Error for user {message.from_user.id}: {error}")
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при поиске фильмов. Попробуйте позже или используйте /low_budget_movie",
        )

    # Сброс состояний
    if SUCCESS:
        bot.reset_data(message.from_user.id, message.chat.id)
        bot.delete_state(message.from_user.id, message.chat.id)
