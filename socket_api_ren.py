# import datetime
# import json
# import os
import requests

from typing import Any
import socketio

# from renpy import config, store
# from renpy.game import persistent

# from game.lovense.LovenseAction_ren import LovenseAction

"""renpy
init python:
"""


class LovenseSocket:
    def __init__(self) -> None:
        self.socket = socketio.Client()

    def get_token(self) -> str:
        return ""

    def validate_authorization(self, auth_token: str) -> dict[str, str]:
        response = requests.post(
            "https://api.lovense-api.com/api/basicApi/getSocketUrl",
            json={"platform": "CrimsonSky", "authToken": str},
        ).json()

        print(response)

        return response["data"]

    def connect(self, url: str) -> None:
        self.socket.connect(url)  # type: ignore

    def get_qr_code(self, auth_token: str) -> str:
        @self.socket.event
        def basicapi_get_qrcode_tc(  # pyright: ignore[reportUnusedFunction]
            data: Any,
        ) -> None:
            print(data)

        self.socket.emit("basicapi_get_qrcode_ts", {"ackId": auth_token})

        return ""
