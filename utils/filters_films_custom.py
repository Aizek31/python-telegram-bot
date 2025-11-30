from config_data.config import RAPID_API_KEY
from typing import Any
from log_config import logger
import requests


headers = {"X-API-KEY": RAPID_API_KEY}


# Получаем все фильмы по ID
@logger.catch
def filter_id_films(films: list[int], params: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Получает список из ID фильмов. Делает запрос по каждому ID, потом фильтрует полученный словарь по заданным ключам

    :param films: список из ID фильмов
    :param params: словарь с параметрами
    :return: возвращает словарь с информацией о фильме
    """

    cinema = []
    for id in films:
        url_film = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}"
        response_film = requests.get(url_film, headers=headers)
        data_2 = response_film.json()
        key_filters = {
            "nameRu",
            "description",
            "ratingImdb",
            "year",
            "genre",
            "ratingAgeLimits",
            "posterUrl",
        }

        # фильтрация словаря по нужным ключам(исключая "genres")
        filtered_dict = {
            key: data_2[key] for key in key_filters if key in data_2 and key != "genres"
        }

        # Обработка жанров: проверяем, есть ли целевой жанр в списке жанров фильма
        genres = [genre["genre"] for genre in data_2.get("genres", [])]

        if params["genre"] in genres:
            filtered_dict["genre"] = params["genre"]
        else:
            filtered_dict["genre"] = None

        # Обработка возрастного рейтинга
        age_limit = filtered_dict.get("ratingAgeLimits", "")
        if age_limit:
            number = "".join(filter(str.isdigit, age_limit)) + "+"
            filtered_dict["ratingAgeLimits"] = number
        else:
            filtered_dict["ratingAgeLimits"] = "Возрастной рейтинг отсутствует"

        cinema.append(filtered_dict)

    return cinema
