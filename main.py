import sys
import time
import asyncio
import telegram
from datetime import datetime
from datetime import time as time_now


from scr.Artelamp import Artelamp_main as ArtlampMain
from scr.Lightstar import Lightstar_main as LightstarMain
from scr.Sonex import Sonex_main as SonexMain
from scr.Stilfort import Stilfort_main as StilfortMain
from scr.Maytoni import Maytoni_main as MaytoniMain


sys.path.append('\\home\\scrapping\\NebesniySvet\\marketplace_yandex-inventory-management.v2')

bot_token = "6589481139:AAG933QoRkfa3s4xuT3Lr4OqvB5QXbSf_qg"
bot = telegram.Bot(token = bot_token)

list_default_for_telegram = ['Maytoni', 'LightStar', 'Sonex', 'Stilfort', 'ArteLamp']
list_success_for_telegram = []

async def make_message_for_tg(some_list, user = 'Артем'):
    
    if user == 'Рома':
        user_name = user
        user_id = 328128719
    elif user == 'Аваг':
        user_name = user
        user_id = 722434246
    else:
        user_name = user
        user_id = 312956486
        user_id_artem = 312956486
    user_id_artem = 312956486
        
    dict_for_tg = {}
    if len(some_list) == 5:
        dict_for_tg[user_id_artem] = f'Остатки {user} - всё окей'
        dict_for_tg[user_id] = 'Сегодня все остатки обновлены'
        return dict_for_tg
    
    elif len(some_list) < 5:
        for item in list_success_for_telegram:
            if item in list_default_for_telegram:
                list_default_for_telegram.remove(item)
        dict_for_tg[user_id_artem] = f'Не отправились {user_name} {", ".join(list_default_for_telegram)}'
        dict_for_tg[user_id] = f'Остатки обновились в {", ".join(some_list)} и не обновились в {", ".join(list_default_for_telegram)}'
        #добавить проверку, что все 5 элементов из list_default_for_telegram
        return dict_for_tg
        
    elif len(some_list) > 5:
        dict_for_tg[user_id_artem] = f'Обнаружен лишний магазин у {user_name}'
        #отправлять какой именно
        return dict_for_tg
    
    else:
        dict_for_tg[user_id_artem] = f'Что-то не так'
        return dict_for_tg
    
async def send_messages_to_users(message_dict):
    for user_id, message in message_dict.items():
        try:
            await bot.send_message(chat_id=user_id, text=message)
            print(f"Сообщение отправлено пользователю с ID {user_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю с ID {user_id}: {e}")

async def main():
    start_api_time = time.time()
    
    try:
        ArtlampMain.main()
        list_success_for_telegram.append('ArteLamp')
        print(f'ArteLampApiMain success, ждём 60c')
        time.sleep(60) 
    except Exception as e:
        print(f'В ScrappingMain ошибка: {e}')
        time.sleep(60) 
        
    try:
        MaytoniMain.main()
        list_success_for_telegram.append('Maytoni')
        print(f'Maytoni success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(e)
        print(f'shit, ждём 120c')
        time.sleep(120) 
        
    try:
        LightstarMain.main()
        list_success_for_telegram.append('LightStar')
        print(f'LightStar success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(e)
        print(f'shit, ждём 120c')
        time.sleep(120) 
        
    try:
        StilfortMain.main()
        list_success_for_telegram.append('Stilfort')
        print(f'StilfortApiMain success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(e)
        print(f'shit, ждём 120c')
        time.sleep(120)
        
    try:
        SonexMain.main()
        list_success_for_telegram.append('Sonex')
        print(f"SonexMain success, ничего не ждём")
    except Exception as e:
        print(e)
        
    time_interval1_start = time_now(9, 45)
    time_interval1_end = time_now(10, 00)
    current_time = datetime.now().time()
        # Проверяем, находится ли текущее время в интервале 18:55 - 23:59 или 00:00 - 08:25
    if (time_interval1_start <= current_time <= time_interval1_end):
                # Если текущее время находится в интервале, устанавливаем множитель цены 0.9
        message_dict = await make_message_for_tg(list_success_for_telegram, 'Аваг')
        await send_messages_to_users(message_dict)  
    else:
            # В других случаях множитель цены остается 1.0
        pass
    

        
    end_api_time = time.time()
    execution_api_time = end_api_time - start_api_time
    print(f"Время выполнения по Api: {execution_api_time} секунд")


if __name__ == '__main__':
    asyncio.run(main())