from typing import Any

from config_data.config import RAPID_API_KEY
from log_config import logger
import requests
import pprint


# Получаем все фильмы по ID
@logger.catch
def filter_id_films(
    films: list[int], params: dict[str, Any], headers: [str, str]
) -> list[dict[str, Any]]:
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
            "ratingKinopoisk",
            "year",
            "genre",
            "ratingAgeLimits",
            "posterUrlPreview",
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


##########################################################################


@logger.catch
def filter_response(films: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Функция отфильтровывает по заданным ключам словарь полученный от API.

    :param dict_films: список полученный от API
    :return: словарь с заданной структурой
    """
    key_filters = [
        "kinopoiskId",
        "nameRu",
        "year",
        "description",
        "genres",
        "posterUrlPreview",
        "ratingAgeLimits",
        "ratingKinopoisk",
    ]

    # Фильтрация фильмов по ключам из запроса API
    filtered_data = []
    for film in films:
        filtered_dict = {key: film.get(key) for key in key_filters}
        filtered_data.append(filtered_dict)

    # Запрос по каждому ID в API и достаем описание каждого фильма присваиваем к ключу без значения из предыдущего отфильтрованного словаря
    # Добавляем описание для каждого фильма. Этот код надо переписать как вспомогательную функцию
    for movie in filtered_data:
        id_movie = movie["kinopoiskId"]
        url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id_movie}"
        headers = {"X-API-KEY": RAPID_API_KEY}
        data_3 = requests.get(url=url, headers=headers)

        # проверка запроса
        try:
            response_2 = data_3.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Не JSON ответ для {id_movie}: {data_3.text[:100]}")
            movie["description"] = "Без описания"
            continue
        # добавление описания к фильму
        if response_2["description"] is not None:
            movie["description"] = response_2["description"].replace("\xa0", " ")
        else:
            movie["description"] = "Без описания"

        # добавление ограничения по возрасту
        age_limit = response_2.get("ratingAgeLimits", "")
        if age_limit is not None:
            number = "".join(filter(str.isdigit, age_limit)) + "+"
            movie["ratingAgeLimits"] = number
        else:
            movie["ratingAgeLimits"] = "Возрастной рейтинг отсутствует"

    return filtered_data


# TODO: вроде нигде не используется, нужно будет удалить
def filter_genres(filtered_data: list[dict[str, Any]]) -> str:
    """
    Функция достает все жанры фильма из словаря и склеивает их в виде единой строки
    :param filtered_data: словарь с данными о фильме.
    :return: Возвращает строку с жанрами
    """
    for cinema in filtered_data:
        genres_str = ", ".join(
            [i["genre"] for i in cinema["genres"]]
        )  # создаем список из жанров и склеиваем их отдельно в строки

    return genres_str


def target_genre(
    output_limit_movie: int, target_genre_user: str, catalog_movie: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Функция фильтрует список фильмов по заданному жанру пользователем.

    :param target_genre_user: (str), целевой жанр
    :param catalog_movie: (list), список фильмов
    :return: (list), отфильтрованный список фильмов по жанру
    """
    filter_movie = []
    id_movie = []

    for movie in catalog_movie:
        genre_film = movie.get("genres", [])
        for i_genre in genre_film:
            genre_name_lower = str(i_genre.get("genre", {})).lower()
            target_lower = target_genre_user.lower()
            if genre_name_lower == target_lower:
                id_kinopoisk = movie.get("kinopoiskId", "")
                if id_kinopoisk not in id_movie:
                    id_movie.append(id_kinopoisk)
                    filter_movie.append(movie)
                break
    filter_movie = filter_movie[:output_limit_movie]

    return filter_movie
