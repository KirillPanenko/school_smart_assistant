# Умный ассистент для школьника

Проект умного голосового ассистента для школьника, работающий на Raspberry Pi 4B с операционной системой Raspbian (Debian).

## Описание

Ассистент активируется нажатием левой кнопки мыши, записывает голосовой запрос пользователя, распознает его с помощью API Сбера, получает ответ от языковой модели GigaChat и озвучивает ответ с помощью синтеза речи.

## Функциональность

- Активация по нажатию левой кнопки мыши
- Запись голоса с микрофона
- Распознавание речи с помощью API Сбера
- Обработка запросов с помощью языковой модели GigaChat
- Синтез речи для озвучивания ответов
- Логирование всех действий

## Требования

- Raspberry Pi 4B (или совместимое устройство)
- Операционная система Raspbian (Debian)
- Python 3.7+
- Микрофон
- Динамики или наушники
- Мышь

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/yourusername/school_smart_assistant.git
   cd school_smart_assistant
   ```

2. Создайте файл конфигурации:
   ```
   cp school_assistant/config/.env.example school_assistant/config/.env
   ```

3. Отредактируйте файл `.env`, добавив свои токены для API:
   ```
   nano school_assistant/config/.env
   ```

4. Запустите скрипт установки и запуска:
   ```
   chmod +x run.sh
   ./run.sh
   ```

## Конфигурация

Для работы ассистента необходимо получить токены доступа:
- Токен для API Сбера (распознавание и синтез речи)
- Токен для GigaChat (языковая модель)

Эти токены нужно указать в файле `school_assistant/config/.env`.

## Использование

1. Запустите ассистента:
   ```
   ./run.sh
   ```

2. Нажмите и удерживайте левую кнопку мыши для начала записи голоса.
3. Задайте вопрос или произнесите команду.
4. Отпустите кнопку, чтобы завершить запись.
5. Дождитесь ответа ассистента.

## Структура проекта

```
school_assistant/
├── api/                  # Модули для работы с внешними API
│   ├── __init__.py
│   └── sber_api.py       # API Сбера для распознавания и синтеза речи
├── audio/                # Модули для работы с аудио
│   ├── __init__.py
│   └── audio_processor.py # Запись и воспроизведение аудио
├── config/               # Конфигурация
│   ├── __init__.py
│   ├── .env.example      # Пример файла с переменными окружения
│   └── config.py         # Загрузка конфигурации
├── hardware/             # Работа с аппаратными средствами
│   ├── __init__.py
│   └── input_devices.py  # Работа с устройствами ввода
├── utils/                # Вспомогательные утилиты
│   ├── __init__.py
│   └── helpers.py        # Вспомогательные функции
├── ai/                   # Модули для работы с ИИ
│   ├── __init__.py
│   └── llm.py            # Работа с языковой моделью
├── __init__.py
└── main.py               # Основной модуль приложения
```

## Лицензия

MIT

## Авторы

Ваше имя