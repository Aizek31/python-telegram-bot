from loguru import logger
import sys

"""
Добавлено логирование кода с уровня "INFO" и вывод в консоль информации
"""


def setup_logger(
    log_file: str = "app.log",
    rotation: str = "10 MB",
    retention: str = "7 days",
    level: str = "INFO",
):
    """
        Настраивает Loguru logger для вывода в консоль и файл с ротацией.

        Функция удаляет стандартный обработчик Loguru и настраивает два новых:
        1. Файл с автоматической ротацией по размеру/времени и удалением старых логов
        2. Цветной вывод в консоль (sys.stderr) с детальной отладочной информацией

        Args:
            log_file (str): Имя файла лога. По умолчанию "app.log"
            rotation (str): Условие ротации файла.
                            Примеры: "10 MB", "500 MB", "1 day", "1 week"
            retention (str): Срок хранения старых логов.
                            Примеры: "7 days", "1 month", "1 year"
            level (str): Минимальный уровень логирования.
                        Возможные значения: "TRACE", "DEBUG", "INFO", "SUCCESS",
                        "WARNING", "ERROR", "CRITICAL"

        Returns:
            loguru.logger: Настроенный объект logger, готовый к использованию

        Example:
            >>> from setup_logger import setup_logger
            >>> log = setup_logger("myapp.log", rotation="5 MB", level="DEBUG")
            >>> log.info("Приложение запущено")
            >>> log.error("Критическая ошибка!")

            Результат:
            - myapp.log: текстовый файл с ротацией
            - Консоль: цветной вывод с временем и уровнем

        Notes:
            - Консольный вывод использует sys.stderr (небуферизировано, видно при редиректе)
            - backtrace=True и diagnose=True включают полную отладочную информацию
            - Функция безопасна для многократного вызова (удаляет предыдущие обработчики)
            - Параметры rotation и retention поддерживают единицы: MB, GB, day, week, month

        Raises:
            ValueError: Если передан некорректный уровень логирования
        """
    logger.remove()  # Удаляем все текущие обработчики (включая стандартный)
    # Добавляем запись ошибок в файл
    logger.add(
        log_file,
        format="{time} {level} {message}",
        level=level,
        rotation=rotation,
        retention=retention,
    )

    # Вывод в консоль
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}",
        colorize=True,
        level=level,
        backtrace=True,
        diagnose=True,
    )

    return logger


# backtrace=True — расширяет трассировку исключения вверх по стеку вызовов, показывая полный стек, который привел к ошибке.
# Это помогает увидеть не только место, где ошибка была поймана, но и весь путь до нее.
#
# diagnose=True — показывает значения всех переменных в контексте каждого фрейма стека при исключении.
# Это облегчает отладку, так как можно увидеть, какие именно данные были в момент ошибки.
