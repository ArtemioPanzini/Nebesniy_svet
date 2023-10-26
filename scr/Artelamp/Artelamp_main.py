import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')) ) #Добавляем корневую папку main для path append


import download_xml_ArteLamp
import send_api_batch_ArteLamp

def main():
    download_xml_ArteLamp.main()
    send_api_batch_ArteLamp.main()


if __name__ == "__main__":
    main()