import requests
import json
import threading
from modules.Nebesniy_svet.scr.Stilfort import xml_to_dict_Stilfort
from modules.Nebesniy_svet.logs import log_file_generator
import config
common_logger = log_file_generator.common_logger


def send_data_batch_price(prices_data):
    
    headers_oauth = {"Authorization": "Bearer y0_AgAAAABW45BlAApomAAAAADrXWqYcge3WjPZQj2l-zlBmGYZGZAehy0"}

    base_url = "https://api.partner.market.yandex.ru/businesses/79508170/offer-prices/updates"
    
    # Разделяем список на батчи по 500 элементов и отправляем каждый батч
    batch_size = 250
    for i in range(0, len(prices_data), batch_size):
        batch = prices_data[i:i + batch_size]

        response = requests.post(base_url, headers=headers_oauth, json={"offers": batch})
        response_data = response.json()
        if response.status_code == 200:
            print(f"Цены Stilfort: Отправлен батч {i // batch_size + 1} Элементы до {i}")
            pass
        else:
            common_logger.info(f'{json.dumps(response_data, indent = 2)}')


def send_data_batch_stock(stocks_data, shop_name, warehouse_api_id):
    
    headers_oauth = config.headers

    base_url = f"https://api.partner.market.yandex.ru/campaigns/{warehouse_api_id}/offers/stocks"
    
    batch_size = 250
    for i in range(0, len(stocks_data), batch_size):
        batch = stocks_data[i:i+batch_size]

        response = requests.put(base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()
        
        if response.status_code == 200:
            print(f"Отправлен батч {i // batch_size + 1} Элементы до {i + batch_size}, магазин {shop_name}")
            pass
        else:
            print(f'Проблемы у {shop_name}', json.dumps(response_data, indent=2))
            

def main():
    prices_data_stilfort, stocks_data_stilfort = xml_to_dict_Stilfort.main()

    thread_prices = threading.Thread(target=send_data_batch_price, args=(prices_data_stilfort,))
    thread_stocks_stilfort = threading.Thread(target=send_data_batch_stock, args=(stocks_data_stilfort,
                                                                                  "Stilfort",
                                                                                  78527993))

    thread_prices.start()
    thread_stocks_stilfort.start()

    thread_prices.join()
    thread_stocks_stilfort.join()
