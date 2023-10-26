
import xml.etree.ElementTree as ET
import os
from datetime import datetime 


from logs import log_file_generator
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
    download_folder = os.path.join(script_directory, '../../data/LightStar/')
    file_path = os.path.join(download_folder, 'LightStar.yml')
    xml_file_path = file_path
    file_path_debug = os.path.join(download_folder, 'list_okay.txt')

    
    list_undebug_correct = read_txt_to_list(file_path_debug)

    prices_data_lightstar = []
    stocks_data_lightstar = []
    try:
        # Разбор XML-файла
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Создание списка для хранения отдельных <offer> элементов
        offers = {}
        date_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')
        
        # Поиск всех элементов <offer>
        for offer_element in root.findall('.//offer'):
            
            article = offer_element.find('.//vendorCode').text
            if article in list_undebug_correct:
                pass
            else:
                continue
            
            
            price_full_str = offer_element.find('.//price').text
            if price_full_str == '-1':
                price_full = 0
            else:
                price_full = float(price_full_str)
                price = round(price_full * 0.899)                
                
            
            # Остатки, не работают
            overleft = 0
                
            try: 
                outlet_element = offer_element.find('.//stock').text
                if outlet_element:
                    overleft = round(float(outlet_element))
                else:
                    overleft = 0
                    
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
            
            # Остатки, не работают
            stocks_data = {
                        "sku": f"{article}",
                        "warehouseId": 807423,
                        "items": [
                            {
                            "count": overleft,
                            "type": "FIT",
                            "updatedAt": date_now,
                            }
                        ]
                        } 
            
            prices_data_lightstar.append(price_data)
            stocks_data_lightstar.append(stocks_data)
            

        return prices_data_lightstar, stocks_data_lightstar

    except Exception as e:
        common_logger.info(f'Ошибка {e}')
        pass
    
if __name__ == "__main__":
    main()

