from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter

if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.polling(timeout=10, long_polling_timeout=20)


"""
config.py — здесь объявляются токены, ключи и другие константы;
states.py — здесь содержатся состояния пользователя;
api.py — отвечает за взаимодействие с API;
main.py — здесь создаются обработчики и запускается бот.
"""


# import telebot
# import time
# from requests.exceptions import ReadTimeout
#
# print(telebot)
#
# bot = telebot.TeleBot(
#     "8497267211:AAHMDSJ3_4oQlII8dpR-kHQ2B2Se1Z_fZK0"
# )  # Токен, полученный от BotFather.
#
#
# @bot.message_handler(commands=["start", "help"])
# def send_welcome(message):
#     bot.reply_to(message, "Hello world!")
#
#
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
#
#
# if __name__ == "__main__":
#     while True:
#         try:
#             bot.infinity_polling(timeout=15)
#             # except ReadTimeout:
#             print("ReadTimeout: Перезапуск polling после ошибки Таймаута чтения")
#             time.sleep(5)  # Пауза перед повторным запуском
#         except Exception as e:
#             print(f"Произошла ошибка: {e}. Перезапуск polling.")
#             time.sleep(5)
