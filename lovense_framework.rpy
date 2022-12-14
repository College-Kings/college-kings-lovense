init python:
    class Lovense():
        @staticmethod
        def vibrate(strength: int, time: float = 0, stop_previous: bool = True):
            data = {
                "command": "Function",
                "action": f"Vibrate:{strength}",
                "timeSec": time,
                "stopPrevious": int(stop_previous),
                "apiVer": 1
            }

            try:
                response = requests.post(f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command", json=data)
            except Exception as e:
                print(e)

        @staticmethod
        def rotate(strength: int, time: int = 0, stop_previous: bool = True):
            data = {
                "command": "Function",
                "action": f"Rotate:{strength}",
                "timeSec": time,
                "stopPrevious": int(stop_previous),
                "apiVer": 1
            }

            try:
                response = requests.post(f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command", json=data)
            except Exception:
                return

        @staticmethod
        def pump(strength: int, time: int = 0, stop_previous: bool = True):
            data = {
                "command": "Function",
                "action": f"Pump:{strength}",
                "timeSec": time,
                "stopPrevious": int(stop_previous),
                "apiVer": 1
            }

            try:
                response = requests.post(f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command", json=data)
            except Exception:
                return
            
        @staticmethod
        def stop():
            data = {
                "command": "Function",
                "action": "Stop",
                "timeSec": 0,
                "apiVer": 1
            }

            try:
                response = requests.post(f"http://{persistent.lovense_local_ip}:{persistent.lovense_http_port}/command", json=data)
            except Exception:
                return
