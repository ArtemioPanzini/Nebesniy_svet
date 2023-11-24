from modules.Nebesniy_svet.scr.Artelamp import download_xml_ArteLamp
from modules.Nebesniy_svet.scr.Artelamp import send_api_batch_ArteLamp


def main():
    download_xml_ArteLamp.main()
    send_api_batch_ArteLamp.main()


if __name__ == "__main__":
    main()
