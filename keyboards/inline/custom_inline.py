from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot


# Внизу это пример кода создания кнопки инлайн
def gen_markup():
    # Создаём объекты кнопок.
    button_1 = InlineKeyboardButton(text="Драма", callback_data="драма")
    button_2 = InlineKeyboardButton(text="Комедия", callback_data="комедия")
    button_3 = InlineKeyboardButton(text="Ужасы", callback_data="ужасы")
    button_4 = InlineKeyboardButton(text="Фантастика", callback_data="фантастика")
    button_5 = InlineKeyboardButton(text="Боевик", callback_data="боевик")
    button_6 = InlineKeyboardButton(text="Романтика", callback_data="романтика")
    button_7 = InlineKeyboardButton(text="Триллер", callback_data="триллер")
    button_8 = InlineKeyboardButton(text="Детектив", callback_data="детектив")
    button_9 = InlineKeyboardButton(text="Вестерн", callback_data="вестерн")
    button_10 = InlineKeyboardButton(text="Фэнтези", callback_data="фэнтези")
    button_11 = InlineKeyboardButton(text="Мюзикл", callback_data="мюзикл")
    button_12 = InlineKeyboardButton(text="Военный", callback_data="военный")

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


# Драма: фокусируется на эмоциональных аспектах и конфликтах персонажей.
# Комедия: призвана вызвать смех и развлечь зрителей.
# Ужасы (хоррор): создают атмосферу страха и напряжения.
# Фантастика: включает элементы научной фантастики и фантазии.
# Боевик: сосредотачивается на динамичных действиях и борьбе.
# Романтика: освещает отношения и эмоциональные переживания персонажей.
# Триллер: содержит элементы напряжения и неопределённости.
# Детектив: сюжет строится вокруг расследования преступлений.
# Вестерн: действия разворачиваются на Диком Западе с ковбоями.
# Фэнтези: основан на магии и вымышленных мирах.
# Мюзикл: повествование сопровождается песнями и танцами.
# Военный: показывает войну и боевые действия.
