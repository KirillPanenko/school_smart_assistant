"""
Модуль для работы с устройствами ввода, такими как кнопки мыши.
"""

from evdev import InputDevice, categorize, ecodes, list_devices


def find_mouse_device():
    """
    Ищет и возвращает устройство мыши.

    Returns:
        InputDevice: Устройство мыши или None, если оно не найдено.
    """
    try:
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
            if "mouse" in device.name.lower():
                return device

        print("Устройство мыши не найдено.")
        return None
    except Exception as e:
        print(f"Ошибка при поиске устройства мыши: {str(e)}")
        return None


def is_left_button_pressed():
    """
    Проверяет, нажата ли левая кнопка мыши.

    Returns:
        bool: True, если левая кнопка нажата, иначе False.
    """
    mouse_device = find_mouse_device()

    if not mouse_device:
        return False

    try:
        # Получаем текущее состояние кнопок
        state = mouse_device.active_keys()
        if ecodes.BTN_LEFT in state:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при получении состояния кнопки: {e}")
        return False
