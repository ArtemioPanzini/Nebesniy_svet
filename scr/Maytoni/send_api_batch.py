import requests
import json
import threading
import time


from logs import log_file_generator
common_logger = log_file_generator.common_logger


import xml_to_dict_maytoni


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
            print(f"Цены: Отправлен батч {i // batch_size + 1} Элементы до {i}")
            # Пауза после отправки 10-го батча на 60 секунд
            if (i // batch_size + 1) == 10:
                print("Пауза на 60 секунд...ждём цены")
                time.sleep(60)  # Подождать 60 секунд
            
        else:
            common_logger.info(f'{json.dumps(response_data, indent = 2)} Майтони')
            
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
    prices_data, stocks_data_maytoni, stocks_data_freya, stocks_data_technical = xml_to_dict_maytoni.main()

    thread_prices = threading.Thread(target=send_data_batch_price, args=(prices_data,))
    thread_stocks_maytoni = threading.Thread(target=send_data_batch_stock, args=(stocks_data_maytoni, "maytoni" , 73335605))
    thread_stocks_freya = threading.Thread(target=send_data_batch_stock, args=(stocks_data_freya, "freya", 73335605))
    thread_stocks_technical = threading.Thread(target=send_data_batch_stock, args=(stocks_data_technical, "technical", 73335605))

    
    thread_prices.start()
    thread_stocks_maytoni.start()
    thread_stocks_freya.start()
    thread_stocks_technical.start()


    # Ожидание завершения потоков
    thread_prices.join()
    thread_stocks_maytoni.join()
    thread_stocks_freya.join()
    thread_stocks_technical.join()