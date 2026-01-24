import os
from datetime import datetime

from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    FloatField,
    DateField,
    AutoField,
)


# Путь к существующей папке database (рядом с ботом)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(SCRIPT_DIR, "my_database")
DB_PATH_SEARCH = os.path.join(DB_DIR, "user_params_database.db")
os.makedirs(DB_DIR, exist_ok=True)

# подключаемся к базе данных database_search.db, если файл отсутствует то будет создан автоматически
db = SqliteDatabase(DB_PATH_SEARCH)


# создаём модель для History
class ModelBase(Model):

    # Дата поиска
    date_search = DateField(default=datetime.now)

    # во внутреннем классе Meta указываем нашу базу данных

    class Meta:
        database = db


class HistorySearch(ModelBase):

    # автоматическое создание уникального ключа в базе данных
    id = AutoField(primary_key=True)
    # это уникальный ключ пользователя
    user_id = IntegerField()
    # Рейтинг фильма
    name_movie = CharField()
    # Жанр фильма
    genre_movie = CharField(null=True, default="неизвестно")
    # количество фильмов для показа
    output = IntegerField()


db.connect()
db.create_tables([HistorySearch], safe=True)
