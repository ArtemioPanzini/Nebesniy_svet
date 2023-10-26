import requests
import json
import threading


from logs import log_file_generator
common_logger = log_file_generator.common_logger

import xml_to_dict_Stilfort


# maytoni 68406114     763847
# freya 71927276       799733
# technical 71951954   800166

def send_data_batch_price(prices_data):
    
    headers_oauth = {"Authorization": "Bearer y0_AgAAAABW45BlAApomAAAAADrXWqYcge3WjPZQj2l-zlBmGYZGZAehy0"}

    Base_url = "https://api.partner.market.yandex.ru/businesses/79508170/offer-prices/updates"
    
    # Разделяем список на батчи по 500 элементов и отправляем каждый батч
    batch_size = 250
    for i in range(0, len(prices_data), batch_size):
        batch = prices_data[i:i + batch_size]

        response = requests.post(Base_url, headers=headers_oauth, json={"offers": batch})
        response_data = response.json()
        if response.status_code == 200:
            print(f"Цены Stilfort: Отправлен батч {i // batch_size + 1} Элементы до {i}")
            pass
        else:
            common_logger.info(f'{json.dumps(response_data, indent = 2)}')
            
def send_data_batch_stock(stocks_data, shop_name, warehouseID):
    
    headers_oauth = {"Authorization": "Bearer y0_AgAAAABW45BlAApomAAAAADrXWqYcge3WjPZQj2l-zlBmGYZGZAehy0"}

    Base_url = f"https://api.partner.market.yandex.ru/campaigns/{warehouseID}/offers/stocks"
    
    batch_size = 250
    for i in range(0, len(stocks_data), batch_size):
        batch = stocks_data[i:i+batch_size]

        response = requests.put(Base_url, headers=headers_oauth, json={"skus": batch})
        response_data = response.json()
        
        if response.status_code == 200:
            print(f"Отправлен батч {i // batch_size + 1} Элементы до {i + batch_size}, магазин {shop_name}")
            pass
        else:
            print(f'Проблемы у {shop_name}',json.dumps(response_data, indent=2))
            

def main():
    prices_data_Stilfort, stocks_data_Stilfort = xml_to_dict_Stilfort.main()

    thread_prices = threading.Thread(target=send_data_batch_price, args=(prices_data_Stilfort,))
    thread_stocks_Stilfort = threading.Thread(target=send_data_batch_stock, args=(stocks_data_Stilfort, "Stilfort" , 75883726))


    
    thread_prices.start()
    thread_stocks_Stilfort.start()


    thread_prices.join()
    thread_stocks_Stilfort.join()
