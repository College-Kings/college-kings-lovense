import os
import requests
from typing import Optional

from renpy import config, store
from renpy.game import persistent

"""renpy
init python:
"""

SERVER_IP = "http://81.100.246.35"


class Lovense:
    @staticmethod
    def vibrate(strength: int, time: float = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Vibrate:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        try:
            requests.post(
                f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command",
                json=data,
            )
        except Exception as e:
            print(e)

    @staticmethod
    def rotate(strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Rotate:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        try:
            requests.post(
                f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command",
                json=data,
            )
        except Exception:
            return

    @staticmethod
    def pump(strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Pump:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        try:
            requests.post(
                f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command",
                json=data,
            )
        except Exception:
            return

    @staticmethod
    def stop() -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": "Stop",
            "timeSec": 0,
            "apiVer": 1,
        }

        try:
            requests.post(
                f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command",
                json=data,
            )
        except Exception:
            return


def get_server_status() -> bool:
    try:
        if requests.get(SERVER_IP, timeout=1).status_code != 200 or True:
            store.lovense_server_status = False
            store.lovense_status_message = (
                "Server Offline. Please connect with Game Mode"
            )
            return False
    except Exception:
        return False


def download_qr_code() -> Optional[str]:
    if not get_server_status():
        return

    try:
        response: requests.Response = requests.post(
            f"{SERVER_IP}/api/v1/lovense/qr_code",
            json={"uid": str(persistent.uuid), "uname": store.name},
        )
        json_content = response.json()

        with open(os.path.join(config.gamedir, "lovense_qr_code.jpg"), "wb") as f:
            f.write(requests.get(json_content["data"]["qr"]).content)
    except Exception as e:
        store.lovense_server_status = False
        print(e)
        return

    return "lovense_qr_code.jpg"


def set_lovense_user() -> None:
    if not get_server_status():
        return

    try:
        response: requests.Response = requests.get(
            f"{SERVER_IP}/api/v1/lovense/users/{persistent.uuid}"
        )

        if response.status_code == 404:
            store.lovense_status_message = (
                "User not found. Please connect with Game Mode"
            )
            return

        lovense_user = response.json()
    except Exception as e:
        store.lovense_server_status = False
        print(e)
        return

    persistent.lovense_http_port = lovense_user["httpPort"]
    persistent.lovense_local_ip = lovense_user["domain"]


lovense_server_status = get_server_status()
lovense_status_message = "Server Offline. Please connect with Game Mode"
persistent.lovense_local_ip = ""
persistent.lovense_http_port = ""
