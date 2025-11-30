import json
from typing import Dict, Union, Any
import requests
from config_data.config import RAPID_API_KEY
from utils.filters_films_custom import filter_id_films
from log_config import logger

# для проверки функции
# params = {"keyword": "халк", "genre": "фантастика", "output": 8}
# headers = {"X-API-KEY": RAPID_API_KEY}


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
        # Название на русском
        id = film.get("filmId", "нет данных")
        id_films.append(id)
    id_films = id_films[: params["output"]]  # фильтруем нужное количество фильмов

    # Функция фильтр по ключевым словам
    output_info_films = filter_id_films(id_films, params)

    return output_info_films


# # Проверка вывода фильма(это я написал для себя)
# a = api_request(params, headers)
# print(json.dumps(a, ensure_ascii=False, indent=4))
