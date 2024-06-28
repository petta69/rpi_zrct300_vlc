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
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(30)
            self._sock.connect(self._location)
        except:
            return False
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
        if not self._connect():
            error_dict = {"ERROR": "Could not make connection to device"}
            self.logger.debug(error_dict)
            return error_dict

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
        return {"Response": response}
        
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
        return self._send_command(command=command)

    def send_power_off(self):
        command = 'power "off"'
        return self._send_command(command=command)

    def send_lightoutput1(self):
        command = 'light_output_val 1'
        return self._send_command(command=command)

    def send_lightoutput2(self):
        command = 'light_output_val 2'
        return self._send_command(command=command)

    def send_lightoutput3(self):
        command = 'light_output_val 3'
        return self._send_command(command=command)

    def send_lightoutput4(self):
        command = 'light_output_val 4'
        return self._send_command(command=command)

    def send_lightoutput5(self):
        command = 'light_output_val 5'
        return self._send_command(command=command)

    def send_lightoutput6(self):
        command = 'light_output_val 6'
        return self._send_command(command=command)

    def send_preset1(self):
        command = 'picture_mode "mode1"'
        return self._send_command(command=command)

    def send_preset2(self):
        command = 'picture_mode "mode2"'
        return self._send_command(command=command)

    def send_preset3(self):
        command = 'picture_mode "mode3"'
        return self._send_command(command=command)

    def send_preset4(self):
        command = 'picture_mode "mode4"'
        return self._send_command(command=command)

    def send_preset5(self):
        command = 'picture_mode "mode5"'
        return self._send_command(command=command)

    def send_preset6(self):
        command = 'picture_mode "mode6"'
        return self._send_command(command=command)

    def send_inputHDMI1(self):
        command = 'input "hdmi1"'
        return self._send_command(command=command)

    def send_inputHDMI2(self):
        command = 'input "hdmi2"'
        return self._send_command(command=command)

    def send_inputDP1(self):
        command = 'input "dp1"'
        return self._send_command(command=command)

    def send_inputDP2(self):
        command = 'input "dp2"'
        return self._send_command(command=command)

    def send_inputDP12(self):
        command = 'input "dp1_2"'
        return self._send_command(command=command)

    def send_PictureMuteOn(self):
        command = 'blank "on"'
        return self._send_command(command=command)

    def send_PictureMuteOff(self):
        command = 'blank "off"'
        return self._send_command(command=command)

    def send_HDR(self):
        command = 'hdr "st2084_sim"'
        return self._send_command(command=command)

    def send_SDR(self):
        command = 'hdr "off"'
        return self._send_command(command=command)

    def send_RealitycreationOn(self):
        command = 'real_cre "on"'
        return self._send_command(command=command)

    def send_RealityCreationOff(self):
        command = 'real_cre "off"'
        return self._send_command(command=command)

    def send_MotionFlowOff(self):
        command = 'motionflow "off"'
        return self._send_command(command=command)

    def send_MotionFlow1(self):
        command = 'motionflow "1"'
        return self._send_command(command=command)

    def send_MotionFlow2(self):
        command = 'motionflow "2"'
        return self._send_command(command=command)

    def send_MotionFlow3(self):
        command = 'motionflow "3"'
        return self._send_command(command=command)

    def send_MotionFlow4(self):
        command = 'motionflow "4"'
        return self._send_command(command=command)

    def send_WideModeNormal(self):
        command = 'aspect "normal"'
        return self._send_command(command=command)

    def send_WideModeFull(self):
        command = 'aspect "full"'
        return self._send_command(command=command)

    def send_WideModeZoom(self):
        command = 'aspect "zoom"'
        return self._send_command(command=command)

    def send_WideModeStretch(self):
        command = 'aspect "stretch"'
        return self._send_command(command=command)

    def send_WideModeNative(self):
        command = 'aspect "native"'
        return self._send_command(command=command)

