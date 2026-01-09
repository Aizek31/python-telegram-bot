from typing import Union, Any
import requests
from utils.filters_films_custom import filter_id_films, target_genre

# from logger_config import logger
from config_data.config import RAPID_API_KEY
from loguru import logger


@logger.catch
def api_request(
    params: dict[str, Union[str, int]], headers: dict[str, str]
) -> list[dict[str, Any]]:
    """
    Функция делает запрос по API сайта кино по введённым параметрам от пользователя и возвращает словарь с нужными данными.

    :param params: словарь параметров запроса с ключами-строками и целочисленными значениями
    :param headers: секретный ключ API

    :return: словарь с результатами запроса
    """

    # ссылка для запроса
    url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword"

    # Получаем фильмы по ключевым словам
    response = requests.get(url, headers=headers, params=params)

    id_films = []
    data = response.json()
    films = data.get("films", [])

    for film in films:
        id = film.get("filmId", "нет данных")
        id_films.append(id)
    # ограничение показа фильмов
    limit = params["output"]
    id_films = id_films[:limit]
    # Функция фильтр по ключевым словам
    output_info_films = filter_id_films(id_films, params, headers)

    return output_info_films


@logger.catch
def api_request_rating(user_info: dict[str, Any]) -> dict[str, Any]:
    url = "https://kinopoiskapiunofficial.tech/api/v2.2/films"
    data = requests.get(url=url, params=user_info, headers=headers)
    query_output = data.json()
    data_dictionary = query_output["items"][0]

    return data_dictionary
