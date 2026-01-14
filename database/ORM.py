from typing import Dict, Any
from .bot_database_films import History, db
from .bot_database_params_search import HistorySearch
from logger_config import setup_logger
from utils.filters_films_custom import filter_genres
from loguru import logger


@logger.catch
def add_history(films: list[dict[str, Any]], user_id: int) -> None:
    """
    Добавляет историю просмотров фильмов в базу данных для пользователя.

    Преобразует данные фильмов из API в формат модели History и выполняет
    пакетную вставку одной транзакцией.

    :param films: Список словарей с данными фильмов (из Kinopoisk API)
    :param user_id: ID пользователя
    :return: None
    """
    # Преобразуйте ключи словарей, если нужно, чтобы соответствовали полям модели
    transformed_films = []
    for film in films:
        if "genre" in film:
            transformed_films.append(
                {
                    "name_movie": film.get("nameRu") or "Неизвестно",
                    "description_movie": film.get("description")
                    or "Описание отсутствует",
                    "rating_movie": film.get("ratingKinopoisk") or 0.0,
                    "year_movie": int(film.get("year", 0)),
                    "genre_movie": film.get("genre") or "неизвестно",
                    "age_limit": int(
                        film.get("ratingAgeLimits", "0")
                        .replace("+", "")
                        .replace("Возрастной рейтинг отсутствует", "0")
                    ),
                    "poster_url": film.get("posterUrlPreview", ""),
                    "user_id": user_id,  # здесь укажите нужный user_id
                }
            )
        elif "genres" in film:
            genres_str = ", ".join([genre["genre"] for genre in film["genres"]])
            transformed_films.append(
                {
                    "name_movie": film.get("nameRu") or "Неизвестно",
                    "description_movie": film.get("description")
                    or "Описание отсутствует",
                    "rating_movie": film.get("ratingKinopoisk") or 0.0,
                    "year_movie": int(film.get("year", "отсутствует")),
                    "genre_movie": genres_str or "неизвестно",
                    "age_limit": int(
                        film.get("ratingAgeLimits", "0")
                        .replace("+", "")
                        .replace("Возрастной рейтинг отсутствует", "0")
                    ),
                    "poster_url": film.get("posterUrlPreview", ""),
                    "user_id": user_id,  # здесь укажите нужный user_id
                }
            )
    # пакетная вставка данных с защитой. Сразу целиком вставляем в таблицу данные одной транзакцией.
    with db.atomic():
        History.insert_many(transformed_films).execute()


# эта функция сохраняет в базе данных введенные пользователем данные для поиска фильма
@logger.catch
def add_history_user_info(info_search: Dict[str, Any], user_id: int) -> None:
    """
    Добавляет данные для поиска фильмов в базу данных.

    :param info_search: Словарь с данными для поиска фильма (из Kinopoisk API)
    :param user_id: ID пользователя
    :return: None
    """
    # Преобразуйте ключи словарей, если нужно, чтобы соответствовали полям модели
    transformed_search_films = []
    transformed_search_films.append(
        {
            "user_id": user_id,  # здесь укажите нужный user_id
            "name_movie": info_search.get("keyword", ""),
            "jenre_movie": info_search.get("genre") or "неизвестно",
            "output": info_search.get("output") or None,
        }
    )
    # пакетная вставка данных с защитой. Сразу целиком вставляем в таблицу данные одной транзакцией.
    with db.atomic():
        HistorySearch.insert_many(transformed_search_films).execute()
