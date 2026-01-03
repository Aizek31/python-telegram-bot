# TODO: здесь нужно реализовать код запроса бюджета фильма
def search_id_genre(genre_from_user: str) -> int:
    """
    Функция, которая ищет id-жанра по целевому жанру , который ввёл пользователь.

    :param genre_from_user: (str), целевой жанр.
    :return: (int), id целевого жанра.
    """

    headers = {"X-API-KEY": RAPID_API_KEY}

    url_1 = "https://kinopoiskapiunofficial.tech/api/v2.2/films/filters"
    data = requests.get(url=url_1, headers=headers)
    response = data.json()

    list_id = response["genres"]

    for id_movie in list_id:
        if id_movie["genre"] == genre_from_user:
            found_genre = id_movie["id"]
            break
    return found_genre


def search_movie(number_genre: int, year_movie: int) -> list[dict[str, Any]]:
    """
    Функция, которая производит поиск фильмов по указанному жанру и году выпуска фильма.

    :param number_genre: (int), id жанра.
    :param year_movie: (int), год выпуска фильма.
    :return: (list), список найденных фильмов.
    """
    RAPID_API_KEY = "64040bc1-bf8c-4c08-bcd4-90f499efd589"
    headers = {"X-API-KEY": RAPID_API_KEY}
    params = {"genres": number_genre, "yearFrom": year_movie, "yearTo": year_movie}
    url_2 = "https://kinopoiskapiunofficial.tech/api/v2.2/films"
    data = requests.get(url=url_2, params=params, headers=headers)
    response = data.json()

    return response.get("items", [])


def low_check_budget(id_movie: list[int]) -> list[int]:
    """
    Функция сортирует низкобюджетные  фильмы и возвращает список id.

    :param id_movie: id фильма
    :return: список id низкобюджетных фильмов
    """
    low_movie = []
    for id in id_movie:
        headers = {"X-API-KEY": RAPID_API_KEY}
        url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}/box_office"
        data = requests.get(url=url, headers=headers)
        response = data.json()
        fundraising = response["items"]

        for keys in fundraising:
            if keys["type"] == "BUDGET" and keys["amount"] < 3000000:
                low_movie.append(id)
    return low_movie


def big_check_budget(id_movie: list[int]) -> list[int]:
    """
    Функция сортирует высокобюджетные  фильмы и возвращает список id.

    :param id_movie: id фильма
    :return: список id высокобюджетных фильмов
    """
    big_movie = []
    for id in id_movie:
        headers = {"X-API-KEY": RAPID_API_KEY}
        url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}/box_office"
        data = requests.get(url=url, headers=headers)
        response = data.json()
        fundraising = response["items"]

        for keys in fundraising:
            if keys["type"] == "BUDGET" and keys["amount"] > 3000000:
                big_movie.append(id)
    return big_movie
