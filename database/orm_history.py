import os
from datetime import date
from typing import Any

from peewee import SqliteDatabase
from database.bot_database_films import History


def get_database() -> SqliteDatabase:
    """Возвращает подключенную базу данных"""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "my_database", "bot_database_films.db")
    db = SqliteDatabase(db_path)
    db.connect()
    return db


def get_all_history(db: SqliteDatabase) -> list[dict[str, Any]]:
    """
    Получить ВСЕ записи истории поиска фильмов

    Returns:
        Список всех записей в виде словарей
    """
    if db is None:
        db = get_database()
        close_db = True
    else:
        close_db = False

    try:
        return list(History.select().dicts())
    finally:
        if close_db:
            db.close()


def get_history_by_date(target_date: date, db: SqliteDatabase) -> list[dict[str, Any]]:
    """
    Получить записи истории поиска за конкретную дату

    Args:
        target_date: Дата поиска (date)
        db: Подключенная база (опционально)

    Returns:
        Список записей за указанную дату
    """
    if db is None:
        db = get_database()
        close_db = True
    else:
        close_db = False

    try:
        return list(History.select().where(History.date_search == target_date).dicts())
    finally:
        if close_db:
            db.close()
