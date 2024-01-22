import datetime
import json
import os
import requests
from typing import Any, ClassVar, Iterable, Optional

from renpy import config, store
from renpy.game import persistent

from game.lovense.LovenseAction_ren import LovenseAction

"""renpy
init python:
"""

SERVER_IP = "http://81.100.246.35"


class Lovense:
    MAX_STRENGTHS: ClassVar[dict[LovenseAction, int]] = {
        LovenseAction.VIBRATE: 20,
        LovenseAction.ROTATE: 20,
        LovenseAction.PUMP: 3,
        LovenseAction.THRUST: 20,
        LovenseAction.FINGER: 20,
        LovenseAction.SUCTION: 20,
        LovenseAction.DEPTH: 3,
        LovenseAction.ALL: 20,
    }

    def __init__(self) -> None:
        self.local_ip: str = ""
        self.http_port: str = ""

        self.last_refresh: datetime.datetime = datetime.datetime.now()

        self.server_status: bool = self.get_server_status()
        self.status_message: str = ""
        self.toys: dict[str, str] = {}
        self.last_updated: int = 0

        self.current_strengths: dict[LovenseAction, int] = {
            action: 0
            for action in LovenseAction
            if action not in (LovenseAction.ALL, LovenseAction.STOP)
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

    def send_function(
        self,
        actions: Iterable[tuple[str, int]],
        time_sec: float = 0,
        stop_previous: bool = True,
    ) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": ",".join(f"{action}:{value}" for action, value in actions),
            "timeSec": time_sec,
            "stopPrevious": int(stop_previous),
            "apiVer": 1,
        }

        self._send_command(data)

    def get_toys(self) -> None:
        data: dict[str, str] = {"command": "GetToys"}

        json_content = self._send_command(data)
        if json_content is None:
            return

        self.toys = json.loads(json_content["data"]["toys"])

    def vibrate(
        self, strength: int, time: float = 0, stop_previous: bool = True
    ) -> None:
        self.send_function((("Vibrate", strength),), time, stop_previous)

        self.current_strengths[LovenseAction.VIBRATE] = strength

    def rotate(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        self.send_function((("Rotate", strength),), time, stop_previous)

        self.current_strengths[LovenseAction.ROTATE] = strength

    def pump(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        self.send_function((("Pump", strength),), time, stop_previous)

        self.current_strengths[LovenseAction.PUMP] = strength

    def thrust(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        self.send_function((("Thrust", strength),), time, stop_previous)

        self.current_strengths[LovenseAction.THRUST] = strength

    def finger(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        self.send_function((("Finger", strength),), time, stop_previous)

        self.current_strengths[LovenseAction.FINGER] = strength

    def suction(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        self.send_function((("Suction", strength),), time, stop_previous)

        self.current_strengths[LovenseAction.SUCTION] = strength

    def depth(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        self.send_function((("Depth", strength),), time, stop_previous)

        self.current_strengths[LovenseAction.DEPTH] = strength

    def all(self, strength: int, time: int = 0, stop_previous: bool = True) -> None:
        self.send_function((("All", strength),), time, stop_previous)

        self.current_strengths = {k: strength for k in self.current_strengths}

    def stop(self) -> None:
        data: dict[str, object] = {
            "command": "Function",
            "action": "Stop",
            "timeSec": 0,
            "apiVer": 1,
        }

        self._send_command(data)

        self.current_strengths = {k: 0 for k in self.current_strengths}

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

    def download_qr_code(self) -> None:
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
                f"{SERVER_IP}/api/v1/lovense/users/{persistent.uuid}"
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
