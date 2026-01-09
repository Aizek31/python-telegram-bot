import os
import sys
from loguru import logger


def setup_logger(
    log_file: str | None = "app.log",
    rotation: str = "10 MB",
    retention: str = "7 days",
    level: str = "DEBUG",
    caller_file: str | None = None,
):
    """
    Настраивает Loguru logger для вывода в консоль и файл с ротацией.

    Функция удаляет стандартный обработчик Loguru и настраивает два новых:
    1. Файл с автоматической ротацией по размеру/времени и удалением старых логов
    2. Цветной вывод в консоль (sys.stderr) с детальной отладочной информацией

    Args:
        log_file (str | None): Имя файла лога.
            - Если задано строкой, используется как есть.
            - Если None, имя формируется по имени вызывающего файла: main.py -> main.log.
        rotation (str): Условие ротации файла.
                        Примеры: "10 MB", "500 MB", "1 day", "1 week"
        retention (str): Срок хранения старых логов.
                        Примеры: "7 days", "1 month", "1 year"
        level (str): Минимальный уровень логирования.
                    Возможные значения: "TRACE", "DEBUG", "INFO", "SUCCESS",
                    "WARNING", "ERROR", "CRITICAL"
        caller_file (str | None): Путь к файлу, из которого вызывают логгер.
                    Обычно передают __file__. Если None, берётся файл с этой функцией.

    Returns:
        loguru.logger: Настроенный объект logger, готовый к использованию.
    """

    # если не передали, считаем, что вызывают из этого же файла
    if caller_file is None:
        caller_file = __file__

    # директория вызывающего файла
    base_dir = os.path.dirname(os.path.abspath(caller_file))

    # если имя лога не задано явно — формируем из имени модуля
    if log_file is None:
        module_name = os.path.splitext(os.path.basename(caller_file))[0]
        log_file = f"{module_name}.log"

    log_path = os.path.join(base_dir, log_file)

    logger.remove()  # Удаляем все текущие обработчики

    # Лог в файл
    logger.add(
        log_path,
        format="{time} {level} {message}",
        level=level,
        rotation=rotation,
        retention=retention,
        enqueue=True,  # Быстро + надежно
        catch=True,
        delay=False,  # Создать файл сразу
    )

    # Вывод в консоль
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | {message}",
        colorize=True,
        level=level,
        backtrace=True,
        diagnose=True,
    )

    return logger
