import xml.etree.ElementTree as ET
import requests
import time as timesleep
import json
from datetime import datetime
import threading
import os
import sys
from datetime import datetime
from datetime import date
from datetime import time


def read_txt_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        my_list = [line.strip() for line in lines]
        return my_list
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None

def send_data_batch(prices_data, headers_oauth):
    Base_url = "https://api.partner.market.yandex.ru/businesses/79508170/offer-prices/updates"
    
    # Разделяем список на батчи по 500 элементов и отправляем каждый батч
    batch_size = 500
    for i in range(0, len(prices_data), batch_size):
        batch = prices_data[i:i + batch_size]

        response = requests.post(Base_url, headers=headers_oauth, json={"offers": batch})
        response_data = response.json()
        if response.status_code == 200:
            pass
        else:
            print(json.dumps(response_data, indent=2))

def send_data_batch_stock(stocks_data, headers_oauth):
    Base_url = "https://api.partner.market.yandex.ru/campaigns/72948906/offers/stocks"
    
    batch_size = 500
    for i in range(0, len(stocks_data), batch_size):
        batch = stocks_data[i:i+batch_size]

        response = requests.put(Base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()
        
        if response.status_code == 200:
            pass
        else:
            print(json.dumps(response_data, indent=2))

def main():
    start_time = datetime.now()

    date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')
    url = "https://isonex.ru/upload/stocks.xml"

    response = requests.get(url)
    timesleep.sleep(1)

    # Создаем список для хранения данных о ценах
    prices_data = []
    stocks_data = []

    script_directory = os.path.dirname(__file__)
    file_path_debug = os.path.join(script_directory, '../../data/Sonex/not_allow_Sonex.txt')


    list_undebug_incorrect = read_txt_to_list(file_path_debug)

    # Проверка на успешное получение файла
    if response.status_code == 200:
        # Разбор XML-данных
        xml_data = response.content
        root = ET.fromstring(xml_data)

        current_time = datetime.now().time()
                
        # Определяем временные интервалы
        time_interval1_start = time(18, 55)
        time_interval1_end = time(23, 59)
        time_interval2_start = time(0, 0)
        time_interval2_end = time(8, 25)
        
        # Проверяем, находится ли текущее время в интервале 18:55 - 23:59 или 00:00 - 08:25
        if (time_interval1_start <= current_time <= time_interval1_end) or (time_interval2_start <= current_time <= time_interval2_end):
                # Если текущее время находится в интервале, устанавливаем множитель цены 0.9
            price_multiplier = 0.9
        else:
            # В других случаях множитель цены остается 1.0
            price_multiplier = 0.899
            
        now = date.today()
        if now.weekday() in [5,6]:
            price_multiplier = 0.9
            
            
        # Итерация по элементам <item>
        for item in root.findall(".//item"):
            article = item.find("article").text
            article = article.replace(" ", "-")
            if article in list_undebug_incorrect:
                continue
            
            price_str = item.find("price").text
            price_int = int(price_str)
            price_multiplied = price_int * price_multiplier
            price = round(price_multiplied)
            
            stock = item.find("stock").text
            if stock == '1' or stock == '-1' or stock == '2' or stock == '3':
                stock = 0

            # Создаем список данных о цене и добавляем его в список
            price_data = {
                "offerId": f"{article}",
                "price": {
                    "value": int(price),
                    "currencyId": "RUR"
                }
            }
            stock_data = {
                        "sku": f"{article}",
                        "warehouseId": 808379,
                        "items": [
                            {
                            "count": stock,
                            "type": "FIT",
                            "updatedAt": date_now,
                            }
                        ]
                        }
            prices_data.append(price_data)
            stocks_data.append(stock_data)

    # Отображаем общее количество элементов для отправки
    headers_oauth = {"Authorization": "Bearer y0_AgAAAABW45BlAApomAAAAADrXWqYcge3WjPZQj2l-zlBmGYZGZAehy0"}
    thread_prices = threading.Thread(target=send_data_batch, args=(prices_data, headers_oauth))
    thread_stocks = threading.Thread(target=send_data_batch_stock, args=(stocks_data, headers_oauth))
    
    thread_prices.start()
    thread_stocks.start()

    # Ожидание завершения потоков
    thread_prices.join()
    thread_stocks.join()    
    
    end_time = datetime.now()

    finally_time = end_time - start_time
    print(f"Sonex {finally_time}")


if __name__ == "__main__":
    main()