import socket
import binascii
import ipaddress
from typing import Optional
from logger.logger import Logger

def validate_ipaddress(host_string):
    try:
        ip_object = ipaddress.ip_address(host_string)
        return ip_object
    except ValueError:
        print(f'ERROR: Could not validate ip: {host_string}')
        return 0

class adcp:
    def __init__(self, port: int, host_ip: str, password: str, verbose=1) -> None:
        self.logger = Logger(name=__name__, level=verbose).get_logger()
        if validate_ipaddress:
            self._location = (host_ip, port)
            self._password = password
            self.logger.debug(f'Will use HOST IP: {self._location}')
        else:
            self.logger.error(f'ERROR: {host_ip} is not a valid IP')
            return False
        
    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(0.5)
        self._sock.connect(self._location)
        ## Get password, if needed
        try:
            ## If we get response we need to use to authenticate
            response = self._receive_response()
            self.logger.debug(response)
            ## TODO: Send response+password to host
        except:
            ## If no response, there is no password needed
            self.logger.debug('No response, most likely no password needed')



    def _close_connection(self):
        self._sock.close()
        
    def _send_command(self, command: str) -> Optional[str]:
        ## First we make the connection
        self._connect()

        ## Now send command
        command = f'{command}\r\n'
        command_binary = str.encode(command, "utf-8")
        self.logger.debug(f'Sending command: {command_binary}')
        
        self._sock.send(command_binary)
        self.logger.debug(self._sock)
        try:
            response = self._receive_response()
            self.logger.debug(f"Response: {response}")
        except:
            response = []
        return response
        
    def _receive_response(self) -> Optional[dict]:
        response_payload = ""
        while True:
            try:
                # # We read 32 bytes at the time
                response = self._sock.recv(32)
                # # Now add to our response_payload
                response_payload = f"{response_payload}{response.decode('utf-8')}"
                self.logger.debug(response)
                # * The message is done when last '}' is receieved
                if response_payload.endswith('\r'):
                    self.logger.debug(response_payload)
                    return response
            except socket.timeout:
                self.logger.error("Could not get answer")
                break    
            

    ##
    ## Defined commands
    ##
    def send_power_on(self):
        command = 'power "on"'
        self._send_command(command=command)