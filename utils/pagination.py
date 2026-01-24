from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardButton

# from utils.filters_films_custom import create_film_caption


# Создание самого пагинатора с кнопками
def send_character_page(character_pages, page=1):

    paginator = InlineKeyboardPaginator(
        len(character_pages), current_page=page, data_pattern="film#{page}"
    )

    # paginator.add_after(
    #     InlineKeyboardButton("Назад", callback_data="Назад"),
    #     InlineKeyboardButton("Вперёд", callback_data="Вперёд"),
    # )

    return paginator.markup
