"""
Модуль для загрузки и управления конфигурацией приложения.
Загружает переменные окружения из файла .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения
load_dotenv(os.path.join(BASE_DIR, "config", ".env"))

# Конфигурация для API Сбера
SBER_AUTH_TOKEN = os.getenv("SBER_AUTH_TOKEN")
SBER_API_SCOPE = "SALUTE_SPEECH_PERS"

# Конфигурация для GigaChat
GIGACHAT_AUTH_TOKEN = os.getenv("GIGACHAT_AUTH_TOKEN")

# Настройки аудио
AUDIO_DEVICE_INDEX = int(os.getenv("AUDIO_DEVICE_INDEX", 3))
AUDIO_RATE = int(os.getenv("AUDIO_RATE", 16000))
AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", 1))
AUDIO_FORMAT = os.getenv("AUDIO_FORMAT", "wav")
OUTPUT_AUDIO_FILE = os.getenv("OUTPUT_AUDIO_FILE", "output.wav")

# Задаем полный путь к аудиофайлу
OUTPUT_AUDIO_PATH = os.path.join(BASE_DIR, "audio", OUTPUT_AUDIO_FILE)

# Системный промпт для LLM
SYSTEM_PROMPT = """Ты ассистент школьника, помогаешь со школьными делами. Ниже приводится дружеский разговор между человеком и AI. AI разговорчив и предоставляет множество конкретных деталей из своего контекста. Если AI не знает ответа на вопрос, он честно говорит, что не знает.
отвечая на вопрос используй информацию из контекста:
контекст: "Расписание на Пятницу : 8:30 - Русский, 9:30 - Математика. Расписание на понедельник: 8:20 - Литература, 9:50 - Инженерное дело"
"информация о школе 777: Государственное бюджетное общеобразовательное учреждение «Инженерно-технологическая школа № 777» Санкт-Петербурга – уникальное образовательное учреждение России с высокотехнологичной образовательной средой, созданное по инициативе Правительства Санкт-Петербурга и Комитета по образованию."
"расписание дополнительных занятий : Во вторник и четверг английский в 16:15"
Если в контексте не достаточно информации отвечай своими словами"""
