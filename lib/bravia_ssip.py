import socket
import ipaddress
from typing import Optional

def validate_ipaddress(host_string):
    try:
        ip_object = ipaddress.ip_address(host_string)
        return ip_object
    except ValueError:
        print(f'ERROR: Could not validate ip: {host_string}')
        return 0
    
class bravia_ssip:
    def __init__(self, host_ip: str, port=20060, verbose=1) -> None:
        if validate_ipaddress:
            self._location = (host_ip, port)
        else:
            return False
        
    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(30)
        self._sock.connect(self._location)
        ## When connection is made we will first get notification on power
        response_notify = self._receive_response()
        ## Next notification transmission is about AudioMute, AudioVol and PictureMute
        response_notify = self._receive_response()        

    def _close_connection(self):
        self._sock.close()
        
    def _send_command(self, command: str, parameter="") -> Optional[str]:
        ## First we make the connection
        self._connect()

        header = "*S"

        ## Check if we have parameter
        if parameter == "": ## If no params then we assume it is a query
            message_type = "E"
            parameter = "################"
        else:
            message_type = "C"

        ## Now send command
        message = f'{header}{message_type}{command}{parameter}\n'
        message_binary = str.encode(message, "utf-8")

        self._sock.send(message_binary)
        try:
            response = self._receive_response()
        except:
            response = []

        ## Close connection
        self._close_connection
        return response
        
    def _receive_response(self) -> Optional[dict]:
        response_payload = ""
        while True:
            try:
                # # We read 96 bytes at the time
                response = self._sock.recv(96)
                # # Now add to our response_payload
                response_payload = f"{response_payload}{response.decode('utf-8')}"
                if response_payload.endswith('\n'):
                    return response_payload
                else: 
                    return response_payload

            except socket.timeout:
                break    
            

    ##
    ## Defined commands
    ##

    def set_power_on(self):
        command = 'POWR'
        parameter = '0000000000000001'
        self._send_command(command=command, parameter=parameter)

    def set_power_off(self):
        command = 'POWR'
        parameter = '0000000000000000'
        self._send_command(command=command, parameter=parameter)

    def set_input_hdmi(self, input):
        command = 'INPT'
        parameter = f'000000010000000{input}'
        self._send_command(command=command, parameter=parameter)

    def get_power(self):
        command = 'POWR'
        self._send_command(command=command)

