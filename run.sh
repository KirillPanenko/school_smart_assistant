#!/bin/bash

# Скрипт для запуска умного ассистента для школьника на Raspberry Pi

# Переходим в директорию проекта
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "Виртуальное окружение не найдено. Создаем его..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Запускаем приложение
echo "Запуск умного ассистента для школьника..."
python run.py 