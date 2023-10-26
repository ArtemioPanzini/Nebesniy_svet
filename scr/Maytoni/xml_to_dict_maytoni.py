
import xml.etree.ElementTree as ET
import os
from datetime import datetime
from datetime import time
from datetime import date


from logs import log_file_generator
common_logger = log_file_generator.common_logger


# Функция для чтения списка товаров из файла
def read_txt_take_list(name_file):
    with open(name_file, "r") as file:
        take_list = [строка.strip() for строка in file.readlines()]
    return take_list

# Считываем списки из файлов


def main():
    script_directory = os.path.dirname(__file__)
    download_folder = os.path.join(script_directory, '../../data/Maytoni/')
    file_path = os.path.join(download_folder, 'Maytoni.yml')
    #discount_avaible = read_txt_take_list(os.path.join(download_folder, 'maytoni_discount.txt'))
    xml_file_path = file_path
    prices_data = []
    stocks_data_maytoni = []
    stocks_data_freya = []
    stocks_data_technical = []
    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        current_time = datetime.now().time()
        
        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')
        
        # Получаем текущее время

        # Определяем временные интервалы
        time_interval1_start = time(18, 55)
        time_interval1_end = time(23, 59)
        time_interval2_start = time(0, 0)
        time_interval2_end = time(8, 25)
        
        # Проверяем, находится ли текущее время в интервале 18:55 - 23:59 или 00:00 - 08:25
        if (time_interval1_start <= current_time <= time_interval1_end) or (time_interval2_start <= current_time <= time_interval2_end):
                # Если текущее время находится в интервале, устанавливаем множитель цены 0.9
            price_multiplier = 0.899
        else:
            # В других случаях множитель цены остается 1.0
            price_multiplier = 0.899
            
        now = date.today()
        if now.weekday() in [5,6]:
            price_multiplier = 0.899


        for offer_element in root.findall('.//offer'):
            
            if offer_element.find('vendor').text == 'Voltega':
                continue
            
            article = offer_element.get('id')
            #if article in discount_avaible:
            #    price_multiplier = 0.899
                
            price_full_str_ = offer_element.find('.//price').text
            price_full_str = price_full_str_.replace(",", ".")
            price_full = float(price_full_str)
            price_multiplied = price_full * price_multiplier
            price = round(price_multiplied)
            
            overleft = 0
            
            try: 
                outlet_element = offer_element.find('.//outlet')
                overleft_wo_round = outlet_element.get('instock')
                if overleft_wo_round == "-1":
                    overleft = 0
                overleft = round(float(overleft_wo_round))
                if overleft == 1 or overleft == 2 or overleft == 3:
                    overleft = 0
            except Exception as e:
                common_logger.info(f'Ошибка {e} во время разбора {article}')
                
            price_data = {
                "offerId": f"{article}",
                "price": {
                    "value": int(price),
                    "currencyId": "RUR"
                }
            }                
            if overleft < 0:
                overleft = 0
                
            stock_data_maytoni = {
                        "sku": f"{article}",
                        "warehouseId": 820300,
                        "items": [
                            {
                            "count": overleft,
                            "type": "FIT",
                            "updatedAt": date_now,
                            }
                        ]
                        } 
            
            stock_data_freya = {
                        "sku": f"{article}",
                        "warehouseId": 820300,
                        "items": [
                            {
                            "count": overleft,
                            "type": "FIT",
                            "updatedAt": date_now,
                            }
                        ]
                        } 
            
            stock_data_technical = {
                        "sku": f"{article}",
                        "warehouseId": 820300,
                        "items": [
                            {
                            "count": overleft,
                            "type": "FIT",
                            "updatedAt": date_now,
                            }
                        ]
                        }             
            
            prices_data.append(price_data)
            
            if offer_element.find('vendor').text in ['Technical', 'Led Strip', 'Outdoor']:
                stocks_data_technical.append(stock_data_technical)
            if offer_element.find('vendor').text == 'Freya':
                stocks_data_freya.append(stock_data_freya)                
            if offer_element.find('vendor').text == 'Maytoni':
                stocks_data_maytoni.append(stock_data_maytoni)
                
        common_logger.info(f'{(len(stocks_data_maytoni))} длина майтони')
        common_logger.info(f'{(len(stocks_data_freya))} длина фрейа')
        common_logger.info(f'{(len(stocks_data_technical))} длина техникал')
        return prices_data, stocks_data_maytoni, stocks_data_freya, stocks_data_technical

    except Exception as e:
        common_logger.info(f'Ошибка {e}')
        pass
        
# Пример использования функции
if __name__ == '__main__':
    main()