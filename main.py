import os

import requests
from dotenv import load_dotenv

from server import run_server


def main():
    load_dotenv()

    data = {
        "token": os.getenv("LOVENSE_TOKEN"),
        "uid": "0001",
        "uname": "OscarSix",
        "utoken": "0001",
        "v": 2
    }

    result = requests.post("https://api.lovense.com/api/lan/getQrCode", data)
    print(result.json()["data"]["qr"])
    run_server()


if __name__ == "__main__":
    main()
