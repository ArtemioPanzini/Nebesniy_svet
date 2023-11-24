from modules.Nebesniy_svet.scr.Maytoni import download_xml_maytoni
from modules.Nebesniy_svet.scr.Maytoni import send_api_batch


def main():
    download_xml_maytoni.main()
    send_api_batch.main()


if __name__ == "__main__":
    main()
