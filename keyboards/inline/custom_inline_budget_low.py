from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


# создания кнопки инлайн
def gen_markup_genre_budget():
    # Создаём объекты кнопок.
    button_1 = InlineKeyboardButton(text="Драма", callback_data="Драма")
    button_2 = InlineKeyboardButton(text="Комедия", callback_data="Комедия")
    button_3 = InlineKeyboardButton(text="Ужасы", callback_data="Ужасы")
    button_4 = InlineKeyboardButton(text="Фантастика", callback_data="Фантастика")
    button_5 = InlineKeyboardButton(text="Боевик", callback_data="Боевик")
    button_6 = InlineKeyboardButton(text="Романтика", callback_data="Романтика")
    button_7 = InlineKeyboardButton(text="Триллер", callback_data="Триллер")
    button_8 = InlineKeyboardButton(text="Детектив", callback_data="Детектив")
    button_9 = InlineKeyboardButton(text="Вестерн", callback_data="Вестерн")
    button_10 = InlineKeyboardButton(text="Фэнтези", callback_data="Фэнтези")
    button_11 = InlineKeyboardButton(text="Мюзикл", callback_data="Мюзикл")
    button_12 = InlineKeyboardButton(text="Военный", callback_data="Военный")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        button_1,
        button_2,
        button_3,
        button_4,
        button_5,
        button_6,
        button_7,
        button_8,
        button_9,
        button_10,
        button_11,
        button_12,
    )
    return keyboard
