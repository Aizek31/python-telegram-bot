from loguru import logger
import sys
import functools

"""
Добавлено логирование кода с уровня "INFO" и вывод в консоль информации
"""
logger.remove()  # Удаляем все текущие обработчики (включая стандартный)

# Добавляем запись ошибок в файл
logger.add(
    "errors.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
)


# Вывод в консоль

logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}",
    colorize=True,
    level="INFO",
    backtrace=True,
    diagnose=True,
)

# backtrace=True — расширяет трассировку исключения вверх по стеку вызовов, показывая полный стек, который привел к ошибке.
# Это помогает увидеть не только место, где ошибка была поймана, но и весь путь до нее.
#
# diagnose=True — показывает значения всех переменных в контексте каждого фрейма стека при исключении.
# Это облегчает отладку, так как можно увидеть, какие именно данные были в момент ошибки.
