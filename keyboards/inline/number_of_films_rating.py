from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def gen_number_markup_rating():
    # Создаём объекты кнопок.
    button_1 = InlineKeyboardButton(text="1", callback_data="1")
    button_2 = InlineKeyboardButton(text="2", callback_data="2")
    button_3 = InlineKeyboardButton(text="3", callback_data="3")
    button_4 = InlineKeyboardButton(text="4", callback_data="4")
    button_5 = InlineKeyboardButton(text="5", callback_data="5")
    button_6 = InlineKeyboardButton(text="6", callback_data="6")
    button_7 = InlineKeyboardButton(text="7", callback_data="7")
    button_8 = InlineKeyboardButton(text="8", callback_data="8")
    button_9 = InlineKeyboardButton(text="9", callback_data="9")
    button_10 = InlineKeyboardButton(text="10", callback_data="10")
    button_11 = InlineKeyboardButton(text="11", callback_data="11")
    button_12 = InlineKeyboardButton(text="12", callback_data="12")
    button_13 = InlineKeyboardButton(text="13", callback_data="13")
    button_14 = InlineKeyboardButton(text="14", callback_data="14")
    button_15 = InlineKeyboardButton(text="15", callback_data="15")
    button_16 = InlineKeyboardButton(text="16", callback_data="16")
    button_17 = InlineKeyboardButton(text="17", callback_data="17")
    button_18 = InlineKeyboardButton(text="18", callback_data="18")
    button_19 = InlineKeyboardButton(text="19", callback_data="19")
    button_20 = InlineKeyboardButton(text="20", callback_data="20")

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
        button_13,
        button_14,
        button_15,
        button_16,
        button_17,
        button_18,
        button_19,
        button_20,
    )
    return keyboard
