from modules.Nebesniy_svet.scr.Lightstar import download_xml_lightstar
from modules.Nebesniy_svet.scr.Lightstar import send_api_batch_lightstar


def main():
    download_xml_lightstar.main()
    send_api_batch_lightstar.main()


if __name__ == "__main__":
    main()
