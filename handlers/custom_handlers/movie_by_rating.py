# Стандартная библиотека
from typing import Any

from black import find_user_pyproject_toml

# Сторонние пакеты
from telebot.types import Message

# Локальные модули проекта (в алфавитном порядке)
from api.api_kinopoisk_rating import api_request_rating
from config_data.config import RAPID_API_KEY
from keyboards.inline import gen_markup_genre, gen_number_markup_rating
from loader import bot
from states.user_information_rating import UserState
from utils.filters_films_custom import target_genre, filter_response
from database.ORM import add_history


@bot.message_handler(commands=["movie_by_rating"])
def ask_movie_rating(message: Message) -> None:
    """
    Обработчик команды /movie_by_rating.
    Устанавливает состояние ожидания ввода названия фильма в FSM.

    :param message: объект сообщения Telegram от пользователя.
    :return: None
    """
    bot.set_state(message.from_user.id, UserState.rating_movie, message.chat.id)
    bot.send_message(message.chat.id, "Пожалуйста, введите рейтинг фильма/сериала:")


@bot.message_handler(state=UserState.rating_movie)
def ask_movie_jenre_for_rating(message: Message) -> None:
    """
    Обрабатывает сообщение с ввёденным рейтингом от пользователя.
    Сохраняет введённый данные пользователя в FSM и переводит состояние на ввод жанра.

    :param message: объект сообщения Telegram от пользователя.
    :return: None
    """

    rating = int(message.text)

    if not (0 < rating <= 10):
        bot.send_message(
            message.chat.id,
            "❌ Рейтинг должен быть в диапазоне от 0 до 10. Попробуйте еще раз:",
        )
        return
    else:
        bot.send_message(
            message.chat.id,
            "Спасибо записали, теперь выберите жанр:",
            reply_markup=gen_markup_genre(),
        )
        bot.set_state(message.from_user.id, UserState.genre_movie, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as user_info:
            user_info["rating_cinema"] = float(message.text)


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data, state=UserState.genre_movie
)
def callback_handler(callback_query) -> None:
    """
    Обрабатывает callback от выбора жанра.
    Сохраняет жанр в FSM и переходит к вводу количества фильмов.

    :param callback_query: CallbackQuery от Telegram.
    :return: None
    """
    with bot.retrieve_data(
        callback_query.from_user.id, callback_query.message.chat.id
    ) as user_info:
        user_info["genre"] = callback_query.data

    bot.edit_message_reply_markup(
        callback_query.from_user.id,
        callback_query.message.message_id,
        reply_markup=None,
    )
    bot.send_message(
        callback_query.from_user.id,
        "Спасибо записали жанр. Теперь введите число сколько фильмов/сериалов показать:",
        reply_markup=gen_number_markup_rating(),
    )
    bot.set_state(
        callback_query.from_user.id,
        UserState.output_films,
        callback_query.message.chat.id,
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data, state=UserState.output_films
)
def finish_callback_handler(callback_query) -> dict[str, Any]:
    """
    Обрабатывает сообщением с лимитом показа фильмов.
    Делает запрос по API и возвращает ответ пользователю.

    :param callback_query: объект сообщения Telegram от пользователя.
    :return: Возвращает словарь для отправки пользователю.
    """
    SUCCESS = False
    with bot.retrieve_data(
        callback_query.from_user.id, callback_query.message.chat.id
    ) as user_info:
        user_info["output"] = int(callback_query.data)
        enter_info = user_info  # создаём копию параметров
        rating_user = enter_info["rating_cinema"]
        params = {"ratingFrom": 0, "ratingTo": rating_user}

    bot.edit_message_reply_markup(
        callback_query.from_user.id,
        callback_query.message.message_id,
        reply_markup=None,
    )
    bot.send_message(
        callback_query.message.chat.id,
        "Спасибо ваш ответ записан. Вот список кино, которое мы нашли по Вашему запросу:",
    )

    headers = {"X-API-KEY": RAPID_API_KEY}
    answer = api_request_rating(params, headers)
    output_limit_film = int(user_info["output"])
    answer_filters = filter_response(answer)
    genre = user_info["genre"]
    user_target_genre = target_genre(output_limit_film, genre, answer_filters)
    # Запись найденных фильмов в базу данных
    add_history(user_target_genre, callback_query.from_user.id)

    # Сброс состояния
    bot.reset_data(callback_query.from_user.id, callback_query.message.chat.id)

    # TODO: это можно переделать в функцию, где из жанров делается список
    for film in user_target_genre:
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
            chat_id=callback_query.message.chat.id,
            photo=film["posterUrlPreview"],
            caption=caption,
            parse_mode="Markdown",
        )
        # Сброс состояний
        if SUCCESS:
            bot.reset_data(message.from_user.id, message.chat.id)
            bot.delete_state(message.from_user.id, message.chat.id)
