# Сторонние пакеты
from telebot.types import Message, InputMediaPhoto

# Локальные модули проекта (в алфавитном порядке)
from api.api_kinopoisk_rating import api_request_rating
from config_data.config import RAPID_API_KEY
from keyboards.inline import gen_markup_genre, gen_number_markup_rating
from loader import bot
from states.user_information_rating import UserState
from utils.filters_films_custom import (
    target_genre,
    filter_response,
    caption_for_rating_budget,
)
from database.orm import add_history
from logger_config import setup_logger
from utils.pagination import send_character_page_rating

# Создание логгер файла
log = setup_logger(log_file=None, caller_file=__file__)


@bot.message_handler(commands=["movie_by_rating"])
def ask_movie_rating(message: Message) -> None:
    """
    Обработчик команды /movie_by_rating.
    Устанавливает состояние ожидания ввода названия фильма в FSM.

    :param message: объект сообщения Telegram от пользователя.
    :return: None
    """
    bot.set_state(message.from_user.id, UserState.rating_movie, message.chat.id)
    bot.send_message(message.chat.id, "🎬 Введите рейтинг фильма/сериала (0-10):")


@bot.message_handler(state=UserState.rating_movie)
def ask_movie_genre_for_rating(message: Message) -> None:
    """
    Обрабатывает сообщение с ввёденным рейтингом от пользователя.
    Сохраняет введённый данные пользователя в FSM и переводит состояние на ввод жанра.

    :param message: объект сообщения Telegram от пользователя.
    :return: None
    """

    rating = float(message.text)

    if not (0.0 < rating <= 10.0):
        bot.send_message(
            message.chat.id,
            "❌ Рейтинг должен быть в диапазоне от 0.0 до 10.0\nПопробуйте еще раз:",
        )
        return
    else:
        bot.send_message(
            message.chat.id,
            "✅ Спасибо! Рейтинг записан 🎬\n" "Теперь выберите жанр фильма: 🎭",
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
        "✅ Спасибо! Жанр записан 🎬\n✨ Теперь введите количество фильмов/сериалов для показа (1-20):",
        reply_markup=gen_number_markup_rating(),
    )
    bot.set_state(
        callback_query.from_user.id,
        UserState.output_films,
        callback_query.message.chat.id,
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.isdigit(),
    state=UserState.output_films,
)
def finish_callback_handler(callback_query) -> None:
    """
    Обрабатывает сообщением с лимитом показа фильмов.
    Делает запрос по API и возвращает ответ пользователю.

    :param callback_query: объект сообщения Telegram от пользователя.
    :return: Возвращает список для отправки пользователю.
    """
    SUCCESS = False
    try:
        with bot.retrieve_data(
            callback_query.from_user.id, callback_query.message.chat.id
        ) as user_info:
            user_info["output"] = int(callback_query.data)
            enter_info = user_info  # создаём копию параметров
            rating_user = enter_info["rating_cinema"]
            params = {"ratingFrom": 0, "ratingTo": rating_user}

            headers = {"X-API-KEY": RAPID_API_KEY}
            answer = api_request_rating(params, headers)
            output_limit_film = int(user_info["output"])
            answer_filters = filter_response(answer)
            genre = user_info["genre"]
            user_target_genre = target_genre(output_limit_film, genre, answer_filters)
            user_info["cinema"] = user_target_genre

        bot.edit_message_reply_markup(
            callback_query.from_user.id,
            callback_query.message.message_id,
            reply_markup=None,
        )
        bot.send_message(
            callback_query.message.chat.id,
            "Спасибо! Ваш ответ записан. 🔍 Ищем фильмы...",
        )

        # headers = {"X-API-KEY": RAPID_API_KEY}
        # answer = api_request_rating(params, headers)
        # output_limit_film = int(user_info["output"])
        # answer_filters = filter_response(answer)
        # genre = user_info["genre"]
        # user_target_genre = target_genre(output_limit_film, genre, answer_filters)

        # rating_text = data["rating_cinema"]
        if user_target_genre:
            bot.send_message(
                callback_query.message.chat.id,
                f"✅ Найдено фильмов c рейтингом {rating_user}: {len(user_target_genre)}",
            )

        else:
            bot.send_message(
                callback_query.message.chat.id,
                f"😔 К сожалению, фильмы c рейтингом {rating_user} не найдены.",
            )
            return

        # Запись найденных фильмов в базу данных
        add_history(user_target_genre, callback_query.from_user.id)

        # TODO: это можно переделать в функцию, где из жанров делается список
        # for film in user_target_genre:
        #     caption = caption_for_rating_budget(film)
        first_cinema = user_target_genre[0]
        caption = caption_for_rating_budget(first_cinema)

        bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=first_cinema["posterUrl"],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=send_character_page_rating(user_target_genre),
        )

    except ValueError:
        bot.send_message(
            callback_query.message.chat.id,
            "❌ Введите рейтинг числом. Попробуйте ещё раз:",
        )

    except Exception as error:
        log.error(f"Error for user {callback_query.from_user.id}: {error}")
        bot.send_message(
            callback_query.message.chat.id,
            "❌ Произошла ошибка при поиске фильмов. Попробуйте позже или используйте /movie_by_rating",
        )


# Обработчик нажатий кнопок
@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.startswith("cinema#")
)
def show_films(callback_query):
    bot.answer_callback_query(callback_query.id)
    page = int(callback_query.data.split("#")[1])

    # Берём сохраненные фильмы
    with bot.retrieve_data(
        callback_query.from_user.id, callback_query.message.chat.id
    ) as user_info:
        films = user_info["cinema"]

    # Показываем фильм номер page (нумерация с 0)
    film = films[page - 1]
    paginator = send_character_page_rating(films, page=page)
    caption = caption_for_rating_budget(film)
    media = InputMediaPhoto(
        media=film["posterUrl"],
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
    bot.reset_data(message.from_user.id, message.chat.id)
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "🔄 Поиск сброшен. Используйте /movie_by_rating")
