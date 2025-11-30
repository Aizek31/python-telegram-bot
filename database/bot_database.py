from datetime import datetime
import sqlite3
import os
from re import search

from config_data.config import BASE_DIR
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    TextField,
    FloatField,
    DateField,
)


# подключаемся к базе данных my_database.db, если файл отсутствует то будет создан автоматически
db = SqliteDatabase("bot_database.db")


# создаём модель для History
class ModelBase(Model):

    # Дата поиска
    date_search = DateField(default=datetime.now())

    # во внутреннем классе Meta указываем нашу базу данных

    class Meta:
        database = db


class History(ModelBase):

    # первичный ключ модели, будет совпадать с Telegram ID. Это значит, что он будет уникальным для всей таблицы.
    user_id = IntegerField(primary_key=True)
    # Название фильма/сериала
    name_movie = CharField()
    # Описание фильма
    description_movie = TextField()
    # Рейтинг фильма
    rating_movie = FloatField()
    # год производства фильма
    year_movie = IntegerField()
    # Жанр фильма
    jenre_movie = CharField()
    # Возрастной рейтинг
    age_limit = IntegerField()
    # Постер фильма
    poster_url = CharField()


# создаём таблицу users в базе данных
# db.create_tables([History])

# Пример записи в историю данных о фильме
# user1 = History(
#     date_search="2025-07-13",
#     name_movie="Халк",
#     description_movie="Учёный превращается в большого зелёного монстра",
#     rating_movie=8.7,
#     year_movie=2002,
#     jenre_movie="фантастика",
#     age_limit=16,
#     poster_url="hulk.ru",
# )
#
# # сохранение данных
# user1.save()
#
# users = User.select()  # получаем список пользователей
# for user in users:
#     print(user.name, user.age)
# Дима 25
# Костя 30


# TODO: этот код пример записи результата запроса по АПИ в базу данных
"""
search_date = datetime.date.today()

for item in data['results']:
    movie = Movie(
        search_date=search_date,
        title=item['title'],
        genre=item['genre'],
        year=int(item['year'])
    )
    movie.save()
"""
