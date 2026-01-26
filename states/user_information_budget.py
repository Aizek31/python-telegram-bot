from telebot.handler_backends import State, StatesGroup

# Создание состояний
"""
State — класс, представляющий конкретное состояние (шаг) в диалоговом сценарии.

StatesGroup — класс, используемый для группировки связанных состояний в один сценарий (группу).

StateFilter — фильтр, который позволяет отфильтровывать сообщения в зависимости от текущего состояния пользователя.
"""


class UserState(StatesGroup):
    genre_cinema = State()
    year_cinema = State()
