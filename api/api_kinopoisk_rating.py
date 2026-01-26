from typing import Any
import requests
from loguru import logger


@logger.catch
def api_request_rating(
    params: dict[str, Any], headers: dict[str, str]
) -> list[dict[str, Any]]:
    """
    Функция делает запрос по API сайта по ввёденным параметрам от пользователя
    :param params: словарь параметров запроса с ключами-строками и целочисленными значениями
    :param headers: секретный ключ API
    :return: словарь с результатами запроса
    """
    url = "https://kinopoiskapiunofficial.tech/api/v2.2/films"
    response = requests.get(url=url, params=params, headers=headers)
    data = response.json()
    info_films = data["items"]

    return info_films
