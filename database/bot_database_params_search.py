# TODO: здесь нужно написать модель для базы данных для параметров поиска, которые вводить пользователь
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

from config_data.config import DB_PATH_SEARCH


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
    jenre_movie = CharField(null=True, default="неизвестно")
    # количество фильмов для показа
    output = IntegerField()


db.connect()
db.create_tables([HistorySearch], safe=True)
