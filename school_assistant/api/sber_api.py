"""
Модуль для работы с API Сбера для синтеза и распознавания речи.
"""

import uuid
import requests
from school_assistant.config.config import (
    SBER_AUTH_TOKEN,
    SBER_API_SCOPE,
    OUTPUT_AUDIO_PATH,
)


def get_token(auth_token=SBER_AUTH_TOKEN, scope=SBER_API_SCOPE):
    """
    Выполняет POST-запрос к эндпоинту для получения токена доступа.

    Args:
        auth_token (str): Токен авторизации, необходимый для запроса.
        scope (str): Область действия запроса API.

    Returns:
        str: Токен доступа или None в случае ошибки.
    """
    # Создаем идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth_token}",
    }

    # Тело запроса
    payload = {"scope": scope}

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        response = requests.post(url, headers=headers, data=payload, verify=False)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"Ошибка получения токена: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Ошибка запроса: {str(e)}")
        return None


def speech_to_text(file_path, token):
    """
    Преобразует речь в текст с помощью API Сбера.

    Args:
        file_path (str): Путь к аудиофайлу.
        token (str): Токен доступа.

    Returns:
        list: Список распознанных фраз или None в случае ошибки.
    """
    # URL для распознавания речи
    url = "https://smartspeech.sber.ru/rest/v1/speech:recognize"

    # Заголовки запроса
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "audio/x-pcm;bit=16;rate=16000",
    }

    try:
        # Открытие аудио файла в бинарном режиме
        with open(file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # Отправка POST запроса
        response = requests.post(url, headers=headers, data=audio_data, verify=False)

        # Обработка ответа
        if response.status_code == 200:
            result = response.json()
            print("Ответ API распознавания речи:", result)
            return result["result"]
        else:
            print(
                f"Ошибка распознавания речи: {response.status_code} - {response.text}"
            )
            return None
    except Exception as e:
        print(f"Ошибка при распознавании речи: {str(e)}")
        return None


def text_to_speech(
    text, token, output_path=OUTPUT_AUDIO_PATH, format="wav16", voice="Bys_24000"
):
    """
    Синтезирует речь из текста с помощью API Сбера.

    Args:
        text (str): Текст для синтеза.
        token (str): Токен доступа.
        output_path (str): Путь для сохранения аудиофайла.
        format (str): Формат аудио.
        voice (str): Голос синтеза.

    Returns:
        bool: True в случае успеха, False в случае ошибки.
    """
    url = "https://smartspeech.sber.ru/rest/v1/text:synthesize"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/text"}
    params = {"format": format, "voice": voice}

    try:
        response = requests.post(
            url, headers=headers, params=params, data=text.encode(), verify=False
        )

        if response.status_code == 200:
            # Сохранение синтезированного аудио в файл
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Аудио успешно синтезировано и сохранено: {output_path}")
            return True
        else:
            print(f"Ошибка синтеза речи: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Ошибка при синтезе речи: {str(e)}")
        return False
