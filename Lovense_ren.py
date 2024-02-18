import datetime
import os
from typing import Any, ClassVar, Iterable, Optional

from renpy import config, store
from renpy.game import persistent
import renpy.exports as renpy

from game._lovense.LovenseAction_ren import LovenseAction

"""renpy
init python:
"""

SERVER_IP = "http://82.9.123.190"


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
            return renpy.fetch(
                f"http://{self.local_ip}:{self.http_port}/command",
                method="POST",
                json=data,
                result="json",
            )
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

        result = self._send_command(data)
        if result is None:
            return

        self.toys = result["data"]["toys"]

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
            renpy.fetch(SERVER_IP, timeout=3)
        except Exception as e:
            print(e)
            self.server_status = False
            self.status_message = "Server Offline. Please connect with Game Mode"
            return False

        self.status_message = ""
        return True

    def download_qr_code(self) -> None:
        if not self.get_server_status():
            return

        try:
            content = renpy.fetch(
                f"{SERVER_IP}/api/v1/lovense/qr_code",
                method="POST",
                json={"uid": str(persistent.uuid), "uname": store.name},
                result="json",
            )

            with open(os.path.join(config.gamedir, "lovense_qr_code.jpg"), "wb") as f:
                f.write(renpy.fetch(content["data"]["qr"]).content)
        except Exception as e:
            self.server_status = False
            print(e)

    def set_user(self) -> None:
        if not self.get_server_status():
            return

        try:
            lovense_user = renpy.fetch(
                f"{SERVER_IP}/api/v1/lovense/users/{persistent.uuid}"
            )
        except Exception as e:
            self.server_status = False
            self.status_message = "User not found."
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
