# TODO: тут будет код для поиска фильмов с низким бюджетом
from typing import Any
from telebot.types import Message

from keyboards.inline import gen_markup_genre
from states.user_information_budjet import UserState
from loader import bot
from api.api_kinopoisk_budget import search_id_genre, search_movie, low_check_budget
from utils.filters_films_custom import filter_response


@bot.message_handler(commands=["low_budget_movie"])
def low_budget_movie(message: Message) -> None:
    """
    Обработчик команды /low_budget_movie.
    Устанавливает состояние ожидания ввода жанра фильма в FSM.

    :param message:
    :return: None
    """
    bot.set_state(message.from_user.id, UserState.genre_cinema, message.chat.id)
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите жанр фильма:",
        reply_markup=gen_markup_genre(),
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data, state=UserState.genre_cinema
)
def callback_handler(callback_query) -> None:
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
        "Спасибо, записали выбранный вами жанр. Теперь введите год выпуска фильма:",
    )
    bot.set_state(
        callback_query.from_user.id,
        UserState.year_cinema,
        callback_query.message.chat.id,
    )


# Финишный обработчик  для бюджета
@bot.message_handler(state=UserState.year_cinema)
def finish_callback_handler(message: Message) -> dict[str, Any]:
    """
    Обрабатывает сообщением с лимитом показа фильмов.
    Делает запрос по API и возвращает ответ пользователю.

    :param callback_query: объект сообщения Telegram от пользователя.
    :return: Возвращает словарь для отправки пользователю.
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["year"] = int(message.text)
        enter_info = data  # создаём копию параметров
        target_genre = enter_info["genre_cinema"]
        year_movie = enter_info["year"]

    bot.send_message(
        message.chat.id,
        "Спасибо ваш ответ записан. Вот список кино, которое мы нашли по Вашему запросу:",
    )

    # Сброс состояния
    bot.reset_data(message.from_user.id, message.chat.id)

    # достаёт id жанра
    id_genre = search_id_genre(target_genre)
    # ищет фильмы по id и году выпуска
    catalog_movie = search_movie(id_genre, year_movie)
    # отбирает низкобюджетные фильмы
    low_budget = low_check_budget(catalog_movie)
    # вывод отфильтрованных фильмов
    filter_movie = filter_response(low_budget)
    # TODO: здесь нужно написать, который записывает результаты поиска в базу данных
    # add_history(user_target_genre, callback_query.from_user.id)
    # TODO: это можно переделать в функцию, где из жанров делается список
    for film in filter_movie:
        # достаем жанры из списка и делаем строки с жанрами через запятую для красивого вывода
        genres = film.get("genres") or []
        genres = [genre["genre"] for genre in genres]
        caption = (
            f"**{film['nameRu']}**, {film['year']}\n"
            f"Жанр: {', '.join(genres) if genres else 'не указан'}\n"
            f"Возрастное ограничение: {film['ratingAgeLimits'] or 'отсутствует'}\n"
            f"Рейтинг Кинопоиска: {film['ratingKinopoisk'] or 'отсутствует'}\n\n"
            f"Описание фильма: *{film["description"]}*"
        )

        bot.send_photo(
            chat_id=message.chat.id,
            photo=film["posterUrlPreview"],
            caption=caption,
            parse_mode="Markdown",
        )
