import datetime
import json
import os
import requests
from typing import Any, Optional

from renpy import config, store
from renpy.game import persistent

"""renpy
init python:
"""

SERVER_IP = "http://81.100.246.35"


class Lovense:
    def __init__(self) -> None:
        self.local_ip: str = ""
        self.http_port: str = ""

        self.last_refresh: datetime.datetime = datetime.datetime.now()

        self.server_status: bool = self.get_server_status()
        self.status_message: str = ""
        self.toys: dict[str, str] = {}
        self.last_updated: int = 0

        self.current_strength: dict[str, int] = {
            "vibrate": 0,
            "rotate": 0,
            "pump": 0,
            "thrust": 0,
            "finger": 0,
            "suction": 0,
        }

    def _send_command(self, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        try:
            response: requests.Response = requests.post(
                f"http://{self.local_ip}:{self.http_port}/command",
                json=data,
            )
            return response.json()
        except Exception:
            return None

    def get_toys(self):
        data: dict[str, str] = {"command": "GetToys"}

        json_content = self._send_command(data)
        if json_content is None:
            return

        self.toys = json.loads(json_content["data"]["toys"])

    def vibrate(
        self, strength: int, time: float = 0, stop_previous: bool = True
    ) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Vibrate:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["vibrate"] = strength

    def rotate(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Rotate:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["rotate"] = strength

    def pump(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Pump:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["pump"] = strength

    def thrust(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Thrusting:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["thrust"] = strength

    def finger(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Fingering:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["finger"] = strength

    def suction(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"Suction:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["suction"] = strength

    def all(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": f"All:{strength}",
            "timeSec": time,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["vibrate"] = strength
        self.current_strength["rotate"] = strength
        self.current_strength["pump"] = strength
        self.current_strength["thrust"] = strength
        self.current_strength["finger"] = strength
        self.current_strength["suction"] = strength

    def stop(self) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": "Stop",
            "timeSec": 0,
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strength["vibrate"] = 0
        self.current_strength["rotate"] = 0
        self.current_strength["pump"] = 0
        self.current_strength["thrust"] = 0
        self.current_strength["finger"] = 0
        self.current_strength["suction"] = 0

    def get_server_status(self) -> bool:
        try:
            if requests.get(SERVER_IP, timeout=1).status_code != 200:
                self.server_status = False
                self.status_message = "Server Offline. Please connect with Game Mode"
                return False
        except Exception:
            return False

        self.status_message = ""
        return True

    def download_qr_code(self) -> Optional[str]:
        if not self.get_server_status():
            return

        try:
            response: requests.Response = requests.post(
                f"{SERVER_IP}/api/v1/lovense/qr_code",
                json={"uid": str(persistent.uuid), "uname": store.name},
            )
            json_content = response.json()

            with open(os.path.join(config.gamedir, "lovense_qr_code.jpg"), "wb") as f:
                f.write(requests.get(json_content["data"]["qr"]).content)
        except requests.exceptions.RequestException as e:
            self.server_status = False
            print(e)

    def set_user(self) -> None:
        if not self.get_server_status():
            return

        try:
            response: requests.Response = requests.get(
                f"{SERVER_IP}/api/v1/lovense/user/{persistent.uuid}"
            )

            if response.status_code == 404:
                self.status_message = "User not found."
                return

            lovense_user = response.json()
        except Exception as e:
            self.server_status = False
            print(e)
            return

        self.http_port = lovense_user["http_port"]
        self.local_ip = lovense_user["domain"]
        self.last_updated = lovense_user["last_update"]

    def refresh(self) -> None:
        self.download_qr_code()
        self.set_user()
        self.get_toys()
        self.last_refresh = datetime.datetime.now()


lovense = Lovense()
