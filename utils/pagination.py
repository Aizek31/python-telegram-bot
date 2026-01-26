from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardButton


def send_character_page(character_pages, page=1):
    """
    Создает пагинацию для каталога фильмов.

    Args:
        character_pages: Список страниц каталога фильмов
        page: Номер текущей страницы (по умолчанию 1)

    Returns:
        InlineKeyboardMarkup: Клавиатура пагинации (data_pattern="film#{page}")
    """
    paginator = InlineKeyboardPaginator(
        len(character_pages), current_page=page, data_pattern="film#{page}"
    )
    return paginator.markup


def send_character_page_rating(character_pages, page=1):
    """
    Создает пагинацию для каталога фильмов с определенным рейтингом.

    Args:
        character_pages: Список страниц каталога фильмов
        page: Номер текущей страницы (по умолчанию 1)

    Returns:
        InlineKeyboardMarkup: Клавиатура пагинации (data_pattern="cinema#{page}")
    """
    paginator = InlineKeyboardPaginator(
        len(character_pages), current_page=page, data_pattern="cinema#{page}"
    )
    return paginator.markup


def send_character_page_budget(character_pages, page=1):
    """
    Создает пагинацию для фильмов определенного бюджета.

    Args:
        character_pages: Список каталога фильмов
        page: Номер текущей страницы (по умолчанию 1)

    Returns:
        InlineKeyboardMarkup: Клавиатура пагинации (data_pattern="movie#{page}")
    """
    paginator = InlineKeyboardPaginator(
        len(character_pages), current_page=page, data_pattern="movie#{page}"
    )
    return paginator.markup


def send_character_page_history(character_pages, page=1):
    """
    Создает пагинацию для фильмов из истории поиска.

    Args:
        character_pages: Список каталога фильмов
        page: Номер текущей страницы (по умолчанию 1)

    Returns:
        InlineKeyboardMarkup: Клавиатура пагинации (data_pattern="catalog_movie#{page}")
    """
    paginator = InlineKeyboardPaginator(
        len(character_pages), current_page=page, data_pattern="catalog_movie#{page}"
    )
    return paginator.markup
