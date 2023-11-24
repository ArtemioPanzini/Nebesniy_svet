import xml.etree.ElementTree as ET
import os
from datetime import datetime
from datetime import time
from datetime import date
from modules.Nebesniy_svet.logs import log_file_generator

common_logger = log_file_generator.common_logger


def read_txt_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        my_list = [line.strip() for line in lines]
        return my_list
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None


def main():
    script_directory = os.path.dirname(__file__)
    download_folder = os.path.join(script_directory, '../../data/')
    file_path = os.path.join(download_folder, 'Artelamp.xml')
    xml_file_path = file_path

    allow_folder = os.path.join(script_directory, '../../data/')
    file_path_allow = os.path.join(allow_folder, 'allow_list.txt')
    list_undebug_correct = read_txt_to_list(file_path_allow)

    prices_data_arte_lamp = []
    stocks_data_arte_lamp = []
    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)

        root = tree.getroot()

        # Создание списка для хранения отдельных <offer> элементов
        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')

        current_time = datetime.now().time()

        # Определяем временные интервалы
        time_interval1_start = time(18, 55)
        time_interval1_end = time(23, 59)
        time_interval2_start = time(0, 0)
        time_interval2_end = time(8, 25)

        # Проверяем, находится ли текущее время в интервале 18:55 - 23:59 или 00:00 - 08:25
        if (time_interval1_start <= current_time <= time_interval1_end) or (
                time_interval2_start <= current_time <= time_interval2_end):
            # Если текущее время находится в интервале, устанавливаем множитель цены 0.9
            price_multiplier = 0.899
        else:
            # В других случаях множитель цены остается 1
            price_multiplier = 1

        now = date.today()
        if now.weekday() in [5, 6]:
            price_multiplier = 0.899

        # Поиск всех элементов <offer>
        for offer_element in root.findall('.//offer'):

            article = offer_element.find('.//vendorCode').text

            article = article.replace(" ", "-").replace(',', '-')
            if article not in list_undebug_correct:
                continue
            try:
                price_full_str_ = offer_element.find('.//price').text

                if price_full_str_ != "0.01":
                    price_full_str = price_full_str_.replace(",", ".")
                    price_full = float(price_full_str)
                    price_multiplied = price_full * price_multiplier
                    price = round(price_multiplied)
                else:
                    price = 1
            except Exception as e:
                common_logger.info(f'Ошибка {e} у {article}')
                price = 0

            overleft = 0
            outlet_element = offer_element.find('.//stock').text

            if outlet_element is not None:

                try:
                    outlet_element = offer_element.find('.//stock').text
                    overleft = round(float(outlet_element))
                    if overleft in (1, 2, 3, 4):
                        overleft = 0
                except Exception as e:
                    common_logger.info(f'Ошибка {e} во время разбора {article}')
                    pass

            price_data = {
                "offerId": f"{article}",
                "price": {
                    "value": int(price),
                    "currencyId": "RUR"
                }
            }

            stocks_data = {
                "sku": f"{article}",
                "warehouseId": 1234240,
                "items": [
                    {
                        "count": overleft,
                        "type": "FIT",
                        "updatedAt": date_now,
                    }
                ]
            }

            prices_data_arte_lamp.append(price_data)

            stocks_data_arte_lamp.append(stocks_data)
        return prices_data_arte_lamp, stocks_data_arte_lamp

    except Exception as e:
        common_logger.info(f'Ошибка {e}')
        pass
