import socket
import binascii
from hashlib import sha256
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
        self._sock.settimeout(30)
        self._sock.connect(self._location)
        response_key = self._receive_response()
        self.logger.debug(response_key)
        ## Get password, if needed
        if response_key == "NOKEY\r\n":
            return True
        else:
            try: 
                ## TODO: Send response+password to host
                str_to_hash = f"{response_key}{self._password}"
                auth_hash = sha256(str_to_hash.encode('us-ascii')).hexdigest()
                auth_hash = f"{auth_hash}\r\n"
                self.logger.debug(f"Hash to send: {auth_hash} Len: {len(auth_hash)}")
                auth_hash_binary = str.encode(auth_hash, "us-ascii")

                self._sock.send(auth_hash_binary)
                response_passwd = self._receive_response()
                self.logger.debug(f"Response: {response_passwd}")
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
                if response_payload.endswith('\r\n'):
                    self.logger.debug(response_payload)
                    return response_payload
                elif len(response_payload) > 7: ## Auth does not give \r
                    self.logger.debug(response_payload)
                    return response_payload
                else: 
                    self.logger.debug(response_payload)
                    return response_payload

            except socket.timeout:
                self.logger.error("Could not get answer")
                break    
            

    ##
    ## Defined commands
    ##
    def send_power_on(self):
        command = 'power "on"'
        self._send_command(command=command)

    def send_power_off(self):
        command = 'power "off"'
        self._send_command(command=command)

    def send_lightoutput1(self):
        command = 'light_output_val 1'
        self._send_command(command=command)

    def send_lightoutput2(self):
        command = 'light_output_val 2'
        self._send_command(command=command)

    def send_lightoutput3(self):
        command = 'light_output_val 3'
        self._send_command(command=command)

    def send_lightoutput4(self):
        command = 'light_output_val 4'
        self._send_command(command=command)

    def send_lightoutput5(self):
        command = 'light_output_val 5'
        self._send_command(command=command)

    def send_lightoutput6(self):
        command = 'light_output_val 6'
        self._send_command(command=command)

    def send_preset1(self):
        command = 'picture_mode "mode1"'
        self._send_command(command=command)

    def send_preset2(self):
        command = 'picture_mode "mode2"'
        self._send_command(command=command)

    def send_preset3(self):
        command = 'picture_mode "mode3"'
        self._send_command(command=command)

    def send_preset4(self):
        command = 'picture_mode "mode4"'
        self._send_command(command=command)

    def send_preset5(self):
        command = 'picture_mode "mode5"'
        self._send_command(command=command)

    def send_preset6(self):
        command = 'picture_mode "mode6"'
        self._send_command(command=command)


