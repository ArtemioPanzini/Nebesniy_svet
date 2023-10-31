import requests
import json

import xml.etree.ElementTree as ET
import os
from datetime import datetime 
from datetime import time
from datetime import date


from logs import log_file_generator
common_logger = log_file_generator.common_logger


def main():
    script_directory = os.path.dirname(__file__)
    download_folder = os.path.join(script_directory, '../../data/Stilfort/')
    file_path = os.path.join(download_folder, "Stilfort.xml")
    xml_file_path = file_path
    
    prices_data_Stilfort = []
    stocks_data_Stilfort = []
    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)

        root = tree.getroot()
                  
        # Создание списка для хранения отдельных <offer> элементов
        bug_price_articles_Stilfort = []
        bug_stocks_articles_Stilfort = []

        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')
        
        current_time = datetime.now().time()
                
        # Получаем текущее время

        # Определяем временные интервалы
        time_interval1_start = time(19, 55)
        time_interval1_end = time(23, 59)
        time_interval2_start = time(0, 0)
        time_interval2_end = time(8, 25)
        
        # Проверяем, находится ли текущее время в интервале 19:55 - 23:59 или 00:00 - 08:25
        if (time_interval1_start <= current_time <= time_interval1_end) or (time_interval2_start <= current_time <= time_interval2_end):
                # Если текущее время находится в интервале, устанавливаем множитель цены 0.9
            price_multiplier = 0.9
        else:
            # В других случаях множитель цены остается 1.0
            price_multiplier = 0.9 


        now = date.today()
        if now.weekday() in [5,6]:
            price_multiplier = 0.9

        # Поиск всех элементов <offer>
        for offer_element in root.findall('.//offer'):
            
            article = offer_element.find('.//Артикул').text
            if article == None:
                continue
            article = article.replace(" ","-").replace("+", "/")
            if article == "2144/09/02W" or article == "2170/05/01W" or article == "3015/02/03C":
                price_full_str = offer_element.find('.//price').text
                price_full = float(price_full_str)
                price_multiplied = price_full * price_multiplier
                price = round(price_multiplied)
                

                overleft = 0
                param_element = offer_element.find('.//param[@name="Остатки"]')
                value = param_element.text


                if value:
                    if value == "более 10":
                        overleft = "11"
                    else:    
                        element_true = value.replace(" ","").replace("шт","")
                            
                        if element_true == None:
                            overleft = "0"
                        elif int(element_true) <= 3:
                            overleft = "0"
                        else:
                            overleft = value
                                                
                price_data_bug = {
                    "offerId": f"{article}",
                    "price": {
                        "value": int(price),
                        "currencyId": "RUR"
                    }
                }              
                            
                stocks_data_bug = {
                            "sku": f"{article}",
                            "warehouseId": 1110688,
                            "items": [
                                {
                                "count": overleft,
                                "type": "FIT",
                                "updatedAt": date_now,
                                }
                            ]
                            }
                
                bug_price_articles_Stilfort.append(price_data_bug)
                bug_stocks_articles_Stilfort.append(stocks_data_bug)
            
            
            
            
            article = article.lower()


            
            price_full_str = offer_element.find('.//price').text
            price_full = float(price_full_str)
            price_multiplied = price_full * price_multiplier
            price = round(price_multiplied)
                
            overleft = 0
            param_element = offer_element.find('.//param[@name="Остатки"]')
            value = param_element.text


            if value:
                if value == "более 10":
                    overleft = "11"
                else:    
                    element_true = value.replace(" ","").replace("шт","")
                        
                    if element_true == None:
                        overleft = "0"
                    elif int(element_true) <= 1:
                        overleft = "0"
                    else:
                        overleft = value
                                            
            price_data = {
                "offerId": f"{article}",
                "price": {
                    "value": int(price),
                    "currencyId": "RUR"
                }
            }              
                        
            stocks_data = {
                        "sku": f"{article}",
                        "warehouseId": 1110688,
                        "items": [
                            {
                            "count": overleft,
                            "type": "FIT",
                            "updatedAt": date_now,
                            }
                        ]
                        }
            
            prices_data_Stilfort.append(price_data)
            stocks_data_Stilfort.append(stocks_data)
            
            
        send_data_batch_price_bug(bug_price_articles_Stilfort)
        send_data_batch_stock_bug(bug_stocks_articles_Stilfort, "Stilfort" , 75883726)
        return prices_data_Stilfort, stocks_data_Stilfort
        
    except Exception as e:
        print(e)
        common_logger.info(f'Ошибка {e}')
        pass
    
    
def send_data_batch_price():
    pass

def send_data_batch_stock():
    pass



def send_data_batch_price_bug(prices_data):
    
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
            
def send_data_batch_stock_bug(stocks_data, shop_name, warehouseID):
    
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