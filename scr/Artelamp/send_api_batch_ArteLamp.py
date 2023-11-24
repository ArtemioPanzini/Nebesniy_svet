import requests
import json
import threading
import time
import re
from modules.Nebesniy_svet.scr.Artelamp import xml_to_dict_ArteLamp
from modules.Nebesniy_svet.logs import log_file_generator
common_logger = log_file_generator.common_logger
import config


def send_data_batch_price(prices_data):
    
    headers_oauth = {"Authorization": "Bearer y0_AgAAAABW45BlAApomAAAAADrXWqYcge3WjPZQj2l-zlBmGYZGZAehy0"}

    base_url = "https://api.partner.market.yandex.ru/businesses/79508170/offer-prices/updates"
    
    # Переменные для управления отправкой запросов
    batch_size = 250
    max_requests_per_minute = 5000
    requests_sent_in_minute = 0
    # Разбиваем prices_data на батчи размером 250
    batches = [prices_data[i:i + batch_size] for i in range(0, len(prices_data), batch_size)]
    
    for batch in batches:
        if requests_sent_in_minute >= max_requests_per_minute:
            print("Достигнут лимит запросов. Ожидание...")  
            time.sleep(60)  # Подождать 1 минуту
            requests_sent_in_minute = 0  # Сбросить счетчик
        response = requests.post(base_url, headers=headers_oauth, json={"offers": batch})
        response_data = response.json()
        
        requests_sent_in_minute += len(batch)  # Увеличить счетчик запросов

        if response.status_code == 200:
            print(f"Цены Artelamp: Отправлен батч с {requests_sent_in_minute} элементами")
            pass
        else:
            common_logger.info(f'{json.dumps(response_data, indent=2)} {requests_sent_in_minute} Артламп')
            errors = response_data["errors"]
            for error in errors:
                message_error = error["message"]
                match = re.search(r'\[(\d+)\]', message_error)
                print(batch[int(match.group(1))])


def send_data_batch_stock(stocks_data, shop_name, warehouse_api_id):
    
    headers_oauth = config.headers

    base_url = f"https://api.partner.market.yandex.ru/campaigns/{warehouse_api_id}/offers/stocks"
    
    # Переменные для управления отправкой запросов
    batch_size = 250
    max_requests_per_minute = 5000
    
    requests_sent_in_minute = 0
    # Разбиваем prices_data на батчи размером 250
    batches = [stocks_data[i:i + batch_size] for i in range(0, len(stocks_data), batch_size)]
    
    for batch in batches:
        if requests_sent_in_minute >= max_requests_per_minute:
            print("Достигнут лимит запросов. Ожидание...")  
            time.sleep(60)  # Подождать 1 минуту
            requests_sent_in_minute = 0  # Сбросить счетчик
        response = requests.put(base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()
        
        requests_sent_in_minute += len(batch)  # Увеличить счетчик запросов

        if response.status_code == 200:
            print(f"Остатки {shop_name}: Отправлен батч с {requests_sent_in_minute} элементами")
            pass
        else:

            common_logger.info(f'{json.dumps(response_data, indent=2)} {requests_sent_in_minute}')
            errors = response_data["errors"]
            for error in errors:
                print(f'{json.dumps(response_data, indent=2)} {requests_sent_in_minute}')


def main():
    prices_data_artelamp, stocks_data_artelamp = xml_to_dict_ArteLamp.main()

    thread_prices = threading.Thread(target=send_data_batch_price,
                                     args=(prices_data_artelamp,))

    thread_stocks_artelamp = threading.Thread(target=send_data_batch_stock,
                                              args=(stocks_data_artelamp,
                                                    "Artelamp", 78527993))

    thread_prices.start()
    thread_stocks_artelamp.start()

    thread_prices.join()
    thread_stocks_artelamp.join()
