"""
Главный модуль приложения умного ассистента для школьника.
"""

import os
import time
import logging
import traceback

from school_assistant.api.sber_api import get_token, speech_to_text, text_to_speech
from school_assistant.audio.audio_processor import record_audio, play_audio
from school_assistant.hardware.input_devices import is_left_button_pressed
from school_assistant.ai.llm import AssistantLLM
from school_assistant.utils.helpers import setup_logging, create_directory_if_not_exists
from school_assistant.config.config import OUTPUT_AUDIO_PATH


class SchoolAssistant:
    """
    Основной класс приложения умного ассистента для школьника.
    """

    def __init__(self):
        """
        Инициализирует объект ассистента.
        """
        # Настраиваем логирование
        self.logger = setup_logging(level=logging.INFO)
        self.logger.info("Инициализация ассистента...")

        # Создаем директорию для аудиофайлов, если она не существует
        audio_dir = os.path.dirname(OUTPUT_AUDIO_PATH)
        create_directory_if_not_exists(audio_dir)

        # Инициализируем языковую модель
        self.logger.info("Инициализация языковой модели...")
        self.llm = AssistantLLM()

        # Получаем токен Сбера для API речи
        self.sber_token = None
        self.update_sber_token()

    def update_sber_token(self):
        """
        Обновляет токен для API Сбера.

        Returns:
            bool: True, если токен успешно получен, иначе False.
        """
        self.logger.info("Получение токена для API Сбера...")
        try:
            self.sber_token = get_token()
            if self.sber_token:
                self.logger.info("Токен для API Сбера успешно получен")
                return True
            else:
                self.logger.error("Не удалось получить токен для API Сбера")
                return False
        except Exception as e:
            self.logger.error(f"Ошибка при получении токена для API Сбера: {str(e)}")
            return False

    def handle_interaction(self):
        """
        Обрабатывает один цикл взаимодействия с пользователем:
        запись голоса, распознавание, получение ответа от LLM, синтез речи, воспроизведение.

        Returns:
            bool: True, если взаимодействие успешно завершено, иначе False.
        """
        try:
            # 1. Запись аудио с микрофона
            self.logger.info("Запись голоса...")
            audio_path = record_audio()
            if not audio_path:
                self.logger.error("Ошибка при записи аудио")
                return False

            # 2. Преобразование речи в текст
            self.logger.info("Распознавание речи...")
            if not self.sber_token:
                if not self.update_sber_token():
                    return False

            speech_text = speech_to_text(audio_path, self.sber_token)
            if not speech_text or len(speech_text) == 0:
                self.logger.error("Речь не распознана")
                return False

            recognized_text = speech_text[0]
            self.logger.info(f"Распознанный текст: {recognized_text}")

            # 3. Получение ответа от языковой модели
            self.logger.info("Получение ответа от LLM...")
            llm_response = self.llm.get_response(recognized_text)
            self.logger.info(f"Ответ LLM: {llm_response}")

            # 4. Синтез речи из текста
            self.logger.info("Синтез речи...")
            if not text_to_speech(llm_response, self.sber_token):
                self.logger.error("Ошибка при синтезе речи")
                return False

            # 5. Воспроизведение аудио
            self.logger.info("Воспроизведение ответа...")
            play_audio()

            self.logger.info("Цикл взаимодействия успешно завершен")
            return True

        except Exception as e:
            self.logger.error(f"Ошибка при обработке взаимодействия: {str(e)}")
            self.logger.error(traceback.format_exc())
            return False

    def run(self):
        """
        Запускает основной цикл работы ассистента.
        """
        self.logger.info("Запуск ассистента. Ожидание нажатия левой кнопки мыши...")

        try:
            while True:
                # Проверяем нажатие кнопки
                if is_left_button_pressed():
                    self.logger.info("Кнопка нажата. Начинаю взаимодействие...")
                    self.handle_interaction()

                    # Небольшая пауза после обработки взаимодействия
                    time.sleep(1)

                # Пауза для снижения нагрузки на CPU
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.logger.info("Получен сигнал прерывания. Завершение работы...")
        except Exception as e:
            self.logger.error(f"Критическая ошибка: {str(e)}")
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info("Ассистент завершил работу")


def main():
    """
    Точка входа в приложение.
    """
    assistant = SchoolAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
