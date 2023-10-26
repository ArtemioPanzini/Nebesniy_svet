import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')) ) #Добавляем корневую папку main для path append


import download_xml_lightstar
import send_api_batch_lightstar

def main():
    download_xml_lightstar.main()
    send_api_batch_lightstar.main()


if __name__ == "__main__":
    main()