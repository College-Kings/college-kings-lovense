init python:
    def get_server_status():
        try:
            if (requests.get("http://ec2-3-8-185-82.eu-west-2.compute.amazonaws.com/api/v1/server/status").status_code != 200):
                persistent.lovense_local_ip = "Server Offline"
                persistent.lovense_http_port = "Please connect with Game Mode"
                return False
        except Exception:
            persistent.lovense_local_ip = "Server Offline"
            persistent.lovense_http_port = "Please connect with Game Mode"
            return False

        return True

    def download_qr_code():
        if not get_server_status():
            return

        try:
            response = requests.post("http://ec2-3-8-185-82.eu-west-2.compute.amazonaws.com/api/v1/lovense/qrCode", json={"uid": str(persistent.uuid), "uname": store.name})
            json_content = response.json()

            with open(os.path.join(config.gamedir, "lovense_qr_code.jpg"), "wb") as f:
                f.write(requests.get(json_content["data"]["qr"]).content)
        except Exception as e:
            persistent.lovense_local_ip = "Server Error"
            persistent.lovense_http_port = "Please connect with Game Mode"
            print(e)
            return

        return "lovense_qr_code.jpg"

    def set_lovense_user():
        if not get_server_status():
            return

        try:
            response = requests.get(f"http://ec2-3-8-185-82.eu-west-2.compute.amazonaws.com/api/v1/lovense/users/{persistent.uuid}")
            
            if response.status_code == 404:
                persistent.lovense_local_ip = "User not found"
                persistent.lovense_http_port = ""
                return

            lovense_user = response.json()
        except Exception as e:
            persistent.lovense_local_ip = "Server Error"
            persistent.lovense_http_port = "Please connect with Game Mode"
            print(e)
            return

        persistent.lovense_http_port = lovense_user["httpPort"]
        persistent.lovense_local_ip = lovense_user["domain"]


    persistent.lovense_local_ip = ""
    persistent.lovense_http_port = ""
