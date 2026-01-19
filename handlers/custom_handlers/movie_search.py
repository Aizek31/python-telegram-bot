from typing import Any
from telebot.types import Message, InputMediaPhoto

from keyboards.inline import gen_markup
from keyboards.inline import gen_number_markup
from states.user_information import UserInfoState
from api.api_kinopoisk import api_request
from config_data.config import RAPID_API_KEY
from loader import bot
from database.ORM import add_history, add_history_user_info
from logger_config import setup_logger
from utils.filters_films_custom import caption_for_search
from utils.pagination import send_character_page


# Файл логирования
log = setup_logger(log_file=None, caller_file=__file__)


# Первый шаг - запрос названия
@bot.message_handler(commands=["movie_search"])
def ask_movie_name(message: Message) -> None:
    """
    Обработчик команды /movie_search.
    Устанавливает состояние ожидания ввода названия фильма в FSM.

    :param message: объект сообщения Telegram от пользователя.
    :return: None
    """
    bot.set_state(message.from_user.id, UserInfoState.keyword, message.chat.id)
    bot.send_message(message.chat.id, "🎥 Пожалуйста, введите название фильма! 🍿")


# Запрос жанра
@bot.message_handler(state=UserInfoState.keyword)
def ask_movie_genre(message: Message) -> None:
    """
    Обрабатывает сообщение с названием фильма.

    Сохраняет введённое название в данные пользователя в FSM и переводит состояние на ввод жанра.

    :param message: объект сообщения Telegram от пользователя.
    :return: None
    """
    bot.send_message(
        message.chat.id,
        "Спасибо! ✅ Записали название.🎥\nТеперь выберите жанр фильма:",
        reply_markup=gen_markup(),
    )
    bot.set_state(message.from_user.id, UserInfoState.genre, message.chat.id)
    # Этот менеджер создает словарь data и записывает туда полученные данных от пользователя
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["keyword"] = message.text


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data, state=UserInfoState.genre
)
def callback_handler(callback_query) -> None:
    # Сохраняем выбранный жанр в FSM
    with bot.retrieve_data(
        callback_query.from_user.id, callback_query.message.chat.id
    ) as data:
        data["genre"] = callback_query.data

    # удаляем клавиатуру
    bot.edit_message_reply_markup(
        callback_query.from_user.id,
        callback_query.message.message_id,
        reply_markup=None,
    )

    bot.send_message(
        callback_query.from_user.id,
        "Спасибо! 🎉 Записали выбранный вами жанр.\nТеперь введите число, сколько фильмов/сериалов показать: 📺✨",
        reply_markup=gen_number_markup(),
    )
    bot.set_state(
        callback_query.from_user.id,
        UserInfoState.output,
        callback_query.message.chat.id,
    )



@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.isdigit(),
    state=UserInfoState.output,
)
def finish_collection_callback_handler(callback_query) -> None:
    """
    Обрабатывает сообщение с лимитом.

    Сохраняет введённый лимит в данные пользователя в FSM. Отправляет запрос по API c введенными данными от пользователя.

    :param callback_query: объект сообщения Telegram от пользователя.
    :return: None
    """
    SUCCESS = False
    try:
        bot.answer_callback_query(callback_query.id)
        with bot.retrieve_data(
            callback_query.from_user.id, callback_query.message.chat.id
        ) as data:
            data["output"] = int(callback_query.data)
            params = data  # создаём копию параметров

        # удаляем клавиатуру
        bot.edit_message_reply_markup(
            callback_query.from_user.id,
            callback_query.message.message_id,
            reply_markup=None,
        )
        bot.send_message(
            callback_query.message.chat.id,
            "Спасибо! Ваш ответ записан. 🔍 Ищем фильмы...",
        )

        headers = {"X-API-KEY": RAPID_API_KEY}
        answer = api_request(params, headers)
        print(answer[5])
        # Сохраняем список фильмов в данные пользователя
        with bot.retrieve_data(
            callback_query.from_user.id, callback_query.message.chat.id
        ) as data:
            data["films"] = answer

        if answer:
            bot.send_message(
                callback_query.message.chat.id, f"✅ Найдено фильмов: {len(answer)}"
            )

        else:
            bot.send_message(
                callback_query.message.chat.id, f"😔 К сожалению, фильмов не найдено."
            )
            return

        # Добавление результатов поиска в базу данных
        add_history_user_info(params, callback_query.from_user.id)
        add_history(answer, callback_query.from_user.id)

        # здесь код вывода информации о найденных фильмах(нужно его переписать как вспомогательную функцию)
        # Сохраняем результаты в глобальную переменную для пагинации
        # (лучше использовать Redis/базу данных для продакшена)
        first_film = answer[0]
        caption = caption_for_search(first_film)

        bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=first_film["posterUrlPreview"],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=send_character_page(answer),
        )
        # SUCCESS = True
    except ValueError:
        bot.send_message(
            callback_query.message.chat.id,
            "❌ Введите рейтинг числом. Попробуйте ещё раз:",
        )

    except Exception as error:
        log.error(f"Error for user {callback_query.from_user.id}: {error}")
        bot.send_message(
            callback_query.message.chat.id,
            "❌ Произошла ошибка при поиске фильмов. Попробуйте позже или используйте /movie_search",
        )

    # Сброс состояний
    if SUCCESS:
        bot.reset_data(callback_query.from_user.id, callback_query.message.chat.id)
        bot.delete_state(callback_query.from_user.id, callback_query.message.chat.id)



# Обработчик нажатий кнопок
@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.startswith("film#")
)
def show_films(callback_query):
    bot.answer_callback_query(callback_query.id)
    page = int(callback_query.data.split("#")[1])

    # Берём сохраненные фильмы
    with bot.retrieve_data(
        callback_query.from_user.id, callback_query.message.chat.id
    ) as data:
        films = data["films"]

    # Показываем фильм номер page (нумерация с 0)
    film = films[page - 1]
    paginator = send_character_page(films, page=page)
    caption = caption_for_search(film)
    media = InputMediaPhoto(
        media=film["posterUrlPreview"],
        caption=caption,  # ✅ Caption передаётся ЧЕРЕЗ InputMediaPhoto
        parse_mode="Markdown",
    )

    bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=media,
        reply_markup=paginator,
    )
