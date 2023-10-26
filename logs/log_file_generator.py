import logging
import os
from datetime import datetime

# Укажите путь к директории, в которой будет создан общий лог-файл
log_directory = os.path.dirname(__file__)

# Создаем имя файла на основе текущей даты и времени
now = datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f'common_log_{timestamp}.txt'
log_path = os.path.join(log_directory, log_filename)

# Создаем логгер
common_logger = logging.getLogger('common_logger')
common_logger.setLevel(logging.INFO)

# Создаем обработчик для записи логов в файл с кодировкой UTF-8
file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Устанавливаем формат для логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Присоединяем обработчик к логгеру и устанавливаем формат
file_handler.setFormatter(formatter)
common_logger.addHandler(file_handler)

# Пример записи лога
common_logger.info('Это сообщение будет записано в общий лог-файл')

# Для других частей программы, используйте common_logger
