# from telegram_bot_pagination import InlineKeyboardPaginator
# from telebot.types import InlineKeyboardButton
# from utils.filters_films_custom import create_film_caption
#
#
# # Создание самого пагинатора  с кнопками
# def send_character_page(character_pages, page=1):
#     film = character_pages[page - 1]
#     paginator = InlineKeyboardPaginator(
#         len(character_pages), current_page=page, data_pattern="character#{page}"
#     )
#
#     paginator.add_after(InlineKeyboardButton("Назад", callback_data="back"))
#     bot.send_photo(
#         chat_id=message.chat.id,
#         reply_markup=paginator.markup,
#         parse_mode="Markdown",
#         caption=create_film_caption(film),
#         photo=film["posterUrlPreview"],
#     )
