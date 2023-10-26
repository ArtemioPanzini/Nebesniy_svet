import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')) ) #Добавляем корневую папку main для path append

import download_xml_Stilfort
import send_api_batch_Stilfort

def main():
    download_xml_Stilfort.main()
    send_api_batch_Stilfort.main()


if __name__ == "__main__":
    main()