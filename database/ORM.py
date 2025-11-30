from typing import Dict, Any
from .bot_database import History, db


def add_history(films: Dict[str, Any], user_id: int) -> None:
    # Преобразуйте ключи словарей, если нужно, чтобы соответствовали полям модели
    transformed_films = []
    for film in films:
        transformed_films.append(
            {
                "name_movie": film.get("nameRu", ""),
                "description_movie": film.get("description") or "Описание отсутствует",
                "rating_movie": film.get("ratingImdb") or 0.0,
                "year_movie": film.get("year", "отсутствует"),
                "jenre_movie": film.get("genre") or "неизвестно",
                "age_limit": int(
                    film.get("ratingAgeLimits", "0")
                    .replace("+", "")
                    .replace("Возрастной рейтинг отсутствует", "0")
                ),
                "poster_url": film.get("posterUrl", ""),
                "user_id": user_id,  # здесь укажите нужный user_id
            }
        )
    # пакетная вставка данных с защитой. Сразу целиком вставляем в таблицу данные одной транзакцией.
    with db.atomic():
        History.insert_many(transformed_films).execute()
