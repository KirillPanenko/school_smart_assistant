"""
Модуль с вспомогательными функциями для приложения.
"""

import os
import logging
from pathlib import Path
from datetime import datetime


def setup_logging(log_dir=None, level=logging.INFO):
    """
    Настраивает логирование для приложения.

    Args:
        log_dir (str): Директория для хранения логов. Если не указана,
                      используется директория logs в корне проекта.
        level (int): Уровень логирования.

    Returns:
        logging.Logger: Объект логгера.
    """
    # Определяем базовую директорию проекта и директорию для логов
    if log_dir is None:
        base_dir = Path(__file__).resolve().parent.parent
        log_dir = os.path.join(base_dir, "logs")

    # Создаем директорию для логов, если она не существует
    os.makedirs(log_dir, exist_ok=True)

    # Формируем имя файла лога с текущей датой и временем
    log_filename = f"assistant_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = os.path.join(log_dir, log_filename)

    # Настраиваем логгер
    logger = logging.getLogger("school_assistant")
    logger.setLevel(level)

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(level)

    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Создаем форматтер для сообщений
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Логирование настроено. Файл лога: {log_filepath}")

    return logger


def create_directory_if_not_exists(directory_path):
    """
    Создает директорию, если она не существует.

    Args:
        directory_path (str): Путь к директории.

    Returns:
        bool: True, если директория создана или уже существует, иначе False.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Ошибка при создании директории {directory_path}: {str(e)}")
        return False
