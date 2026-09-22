import http.client
import json
import ipaddress
import socket
from logger.logger import Logger
import sys


def validate_ipaddress(host_string):
    try:
        ip_object = ipaddress.ip_address(host_string)
        return ip_object
    except ValueError:
        print(f'ERROR: Could not validate ip: {host_string}')
        return 0

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This target doesn't need to be reachable; it just triggers the routing logic
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

class novastar:
    def __init__(self, host_port: int, host_ip: str, verbose=1) -> None:
        self.logger = Logger(name=__name__, level=verbose).get_logger()
        if validate_ipaddress(host_ip):
            self.host_ip = host_ip
            self.host_port = host_port
            self.verbose = verbose
            self.logger.info(f'Will use HOST IP: {self.host_ip}:{self.host_port}')
            self._screenId = self._connect()
        else:
            self.logger.error(f'ERROR: {host_ip} is not a valid IP')
            return False

    def _connect(self):
        self.screenId = ""
        conn = http.client.HTTPConnection(self.host_ip, self.host_port, timeout=5)
        payload = ''
        headers = {
        'Device-Key': f'{get_local_ip()}',
        'Content-type': 'application/json'
        }
        try:
            if self.verbose > 3:
                print(f"DEBUG: Requesting screen info from {self.host_ip}:{self.host_port}")
                print(f"DEBUG: Headers: {headers} Payload: {payload}")
            conn.request("GET", "/api/v1/screen", payload, headers)
            res = conn.getresponse()
            data = res.read().decode()
            json_data = json.loads(data)
        except:
            print("ERROR: Could not connect to host")
            return {'message': "ERROR: Could not connect to host", 'status': 500}


        if 'data' in json_data:
            if 'screens' in json_data['data']:
                if len(json_data['data']['screens']) == 1:
                    self.screenId = json_data['data']['screens'][0]['screenID']
        return self.screenId


    def _sendCommand(self, method: str, path: str, payload: str):
        conn = http.client.HTTPConnection(self.host_ip, self.host_port, timeout=5)
        headers = {
        'Device-Key': '192.168.0.28',
        'Content-type': 'application/json'
        }
        try:
            if self.verbose > 3:
                print(f"DEBUG: Method: {method} Path: {path} Header: {headers} Payload: {payload}")
            conn.request(method, path, payload, headers)
            res = conn.getresponse()
            data = res.read().decode()
            json_data = json.loads(data)
        except:
            print("ERROR: Could not connect to host")
            return {'message': "ERROR: Could not connect to host", 'status': 500}

        return json_data

    def _requestCommand(self, path: str, payload: str):
        conn = http.client.HTTPConnection(self.host_ip, self.host_port)
        headers = {
        'Device-Key': '192.168.0.28',
        'Content-type': 'application/json'
        }
        try:
            conn.request("GET", path, payload, headers)
            res = conn.getresponse()
            data = res.read().decode()
            json_data = json.loads(data)
        except:
            print("ERROR: Could not connect to host")
            return {'message': "ERROR: Could not connect to host", 'status': 500}

        return json_data


    def send_ApplyPreset(self, preset=0):
        screenId = self._screenId
        payload = json.dumps({
            "sequenceNumber": preset,
            "screenID": screenId
        })
        path = f"/api/v1/preset/current/update"
        return self._sendCommand('POST',path, payload)

    def send_ApplyDisplayNormal(self):
        payload = json.dumps({
            "value": 0,
            "canvasIDs": [0]
        })
        path = f"/api/v1/device/displaymode"
        return self._sendCommand('PUT',path, payload)

    def send_ApplyDisplayBlackOut(self):
        payload = json.dumps({
            "value": 1,
            "canvasIDs": [0]
        })
        path = f"/api/v1/device/displaymode"
        return self._sendCommand('PUT',path, payload)

    def send_ApplyDisplayFreeze(self):
        payload = json.dumps({
            "value": 2,
            "canvasIDs": [0]
        })
        path = f"/api/v1/device/displaymode"
        return self._sendCommand('PUT',path, payload)


    def get_InputSource(self):
        screenId = self._screenId
        payload = json.dumps({
        })
        path = f"/api/v1/device/input/sources"
        return self._requestCommand(path, payload)



if(__name__) == '__main__':
    novastar_controller = novastar(host_port=8001, host_ip="192.168.0.100", verbose=1)
    print(f"ScreenID: {novastar_controller._screenId}")
    print(novastar_controller.send_ApplyPreset(preset=1))
    print(novastar_controller.send_ApplyDisplayNormal())
