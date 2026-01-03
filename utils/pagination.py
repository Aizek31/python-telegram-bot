from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardButton

# Создание самого пагинатора  с кнопками
def send_character_page(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(character_pages), current_page=page, data_pattern="character#{page}"
    )

    paginator.add_before(
        InlineKeyboardButton("Like", callback_data="like#{}".format(page)),
        InlineKeyboardButton("Dislike", callback_data="dislike#{}".format(page)),
    )
    paginator.add_after(InlineKeyboardButton("Go back", callback_data="back"))

    bot.send_message(
        message.chat.id,
        character_pages[page - 1],
        reply_markup=paginator.markup,
        parse_mode="Markdown",