import sys
import time

from scr.Artelamp import Artelamp_main as ArtlampMain
from scr.Lightstar import Lightstar_main as LightstarMain
from scr.Sonex import Sonex_main as SonexMain
from scr.Stilfort import Stilfort_main as StilfortMain
from scr.Maytoni import Maytoni_main as MaytoniMain


sys.path.append('\\home\\scrapping\\NebesniySvet\\marketplace_yandex-inventory-management.v2')


def main():
    start_api_time = time.time()
    
    try:
        ArtlampMain.main()
        print(f'ArteLampApiMain success, ждём 60c')
        time.sleep(60) 
    except Exception as e:
        print(f'В ScrappingMain ошибка: {e}')
        time.sleep(60) 
        
    try:
        MaytoniMain.main()
        print(f'Maytoni success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(e)
        print(f'shit, ждём 120c')
        time.sleep(120) 
        
    try:
        LightstarMain.main()
        print(f'LightStar success, ждём 60c')
        time.sleep(60)
    except Exception as e:
        print(e)
        print(f'shit, ждём 120c')
        time.sleep(120) 
    
    try:
        SonexMain.main()
        print(f"SonexMain success, ничего не ждём")
    except Exception as e:
        print(e)
        
    try:
        StilfortMain.main()
        print(f'StilfortApiMain success, ждём 60c')
    except Exception as e:
        print(e)
        print(f'shit, ждём 120c')
        time.sleep(120)
    

        
    end_api_time = time.time()
    execution_api_time = end_api_time - start_api_time
    print(f"Время выполнения по Api: {execution_api_time} секунд")


if __name__ == '__main__':
    main()