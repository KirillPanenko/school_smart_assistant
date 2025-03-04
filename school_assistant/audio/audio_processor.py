"""
Модуль для работы с аудио: запись с микрофона и воспроизведение.
"""

import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play

from school_assistant.config.config import (
    AUDIO_DEVICE_INDEX,
    AUDIO_RATE,
    AUDIO_CHANNELS,
    OUTPUT_AUDIO_PATH,
)
from school_assistant.hardware.input_devices import is_left_button_pressed


def record_audio(
    output_path=OUTPUT_AUDIO_PATH,
    device_index=AUDIO_DEVICE_INDEX,
    rate=AUDIO_RATE,
    channels=AUDIO_CHANNELS,
    max_seconds=20,
):
    """
    Записывает аудио с микрофона, пока нажата левая кнопка мыши.

    Args:
        output_path (str): Путь для сохранения аудиофайла.
        device_index (int): Индекс устройства записи.
        rate (int): Частота дискретизации.
        channels (int): Количество каналов.
        max_seconds (int): Максимальная длительность записи в секундах.

    Returns:
        str: Путь к записанному аудиофайлу или None в случае ошибки.
    """
    try:
        p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio
        print("Начинаю запись...")

        chunk_size = 1024
        audio_format = pyaudio.paInt16

        stream = p.open(
            format=audio_format,
            channels=channels,
            rate=rate,
            frames_per_buffer=chunk_size,
            input_device_index=device_index,
            input=True,
        )

        frames = []  # Инициализировать массив для хранения кадров

        # Хранить данные в блоках в течение заданного времени
        for i in range(0, int(rate / chunk_size * max_seconds)):
            data = stream.read(chunk_size)
            frames.append(data)

            # Проверяем каждые ~20 чанков (~0.5 секунды при rate=16000)
            if i % 20 == 0:
                if not is_left_button_pressed():
                    print("Запись остановлена (кнопка отпущена)")
                    break

        # Остановить и закрыть поток
        stream.stop_stream()
        stream.close()

        # Завершить интерфейс PortAudio
        p.terminate()

        print("Запись завершена!")

        # Сохранить записанные данные в виде файла WAV
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b"".join(frames))

        return output_path

    except Exception as e:
        print(f"Ошибка при записи аудио: {str(e)}")
        return None


def play_audio(file_path=OUTPUT_AUDIO_PATH):
    """
    Воспроизводит аудиофайл.

    Args:
        file_path (str): Путь к аудиофайлу для воспроизведения.

    Returns:
        bool: True в случае успеха, False в случае ошибки.
    """
    try:
        audio = AudioSegment.from_file(file_path, format="wav")
        play(audio)
        print(f"Файл '{file_path}' успешно воспроизведен.")
        return True
    except Exception as e:
        print(f"Произошла ошибка при воспроизведении аудио: {e}")
        return False
