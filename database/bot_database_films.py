from datetime import datetime, date, timedelta

from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    TextField,
    FloatField,
    DateField,
    AutoField,
    fn,
)

from config_data.config import DB_PATH
import os

# подключаемся к базе данных my_database.db, если файл отсутствует то будет создан автоматически
db = SqliteDatabase(DB_PATH)


# создаём модель для History
class ModelBase(Model):

    # Дата поиска
    date_search = DateField(default=lambda: date.today())

    # во внутреннем классе Meta указываем нашу базу данных

    class Meta:
        database = db


class History(ModelBase):

    # автоматическое создание уникального ключа в базе данных
    id = AutoField(primary_key=True)
    # это уникальный ключ пользователя
    user_id = IntegerField()
    # Название фильма/сериала
    name_movie = CharField(null=True, default=None)
    # Описание фильма
    description_movie = TextField()
    # Рейтинг фильма
    rating_movie = FloatField()
    # год производства фильма
    year_movie = IntegerField(null=True, default="неизвестно")
    # Жанр фильма
    genre_movie = CharField(null=True, default="неизвестно")
    # Возрастной рейтинг
    age_limit = IntegerField()
    # Постер фильма
    poster_url = CharField()


db.connect()
db.create_tables([History], safe=True)


records = History.select(History.name_movie, History.date_search)

print(f"Записей в таблице: {History.select().count()}")
print("SQL запрос:", records.sql())  # Только SQL
print("Данные:")
for record in records:  # ← Выполняет запрос
    print(record.name_movie, record.date_search.date())
