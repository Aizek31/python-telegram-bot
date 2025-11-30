import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

# путь к базе данных
DB_PATH = "database.db"
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
# поддерживаемые команды
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", "поиск фильма/сериала по названию"),
    ("movie_by_rating", "поиск фильмов/сериалов по рейтингу"),
    ("low_budget_movie", "поиск фильмов/сериалов с низким бюджетом"),
    ("high_budget_movie", "поиск фильмов/сериалов с высоким бюджетом"),
    ("history", "возможность просмотра истории запросов и поиска фильма/сериала"))




# # формат назначенной даты у задачи
# DATE_FORMAT = "%d.%m.%Y"
# # Путь абсолютный к базе данных
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
