import requests
from requests.auth import HTTPDigestAuth
import ipaddress
import sys



def validate_ipaddress(host_string):
    try:
        ip_object = ipaddress.ip_address(host_string)
        return ip_object
    except ValueError:
        print(f'ERROR: Could not validate ip: {host_string}')
        return 0
    
def inqanswer_to_dict(inqanswer):
    answer_list = inqanswer.split('&')
    answer_dict = {}
    for item in answer_list:
        line = item.split('=')
        answer_dict[line[0]] = line[1]
    return answer_dict
    
class srg_cgi:
    def __init__(self, host_ip: str, user: str, password: str, port=80, verbose=1) -> None:
        self.logger = Logger(name=__name__, level=verbose).get_logger()
        if validate_ipaddress(host_string=host_ip):
            self._host_ip = host_ip
            self._headers = {'referer': f'http://{host_ip}'}
            self._port = port
            self._digestauth = HTTPDigestAuth(user, password)
            self.logger.debug(f'Will use HOST IP: {self._host_ip}:{self._port}')
        else:
            self.logger.error(f'ERROR: {host_ip} is not a valid IP')
            return False
    
    def _send_inq_command(self, cgi, parameter):
        if cgi == 'ptzautoframing.cgi':
            command = 'analytics'
        elif cgi == 'ptzautoframingexe.cgi':
            command = 'analytics'
        else:
            command = 'command'
        r = requests.get(f'http://{self._host_ip}/{command}/{cgi}', params=parameter, auth=self._digestauth, headers=self._headers)
        self.logger.info(f'Trying: {r.url}')
        self.logger.info(f'Status: {r.status_code}')
        
        if r.status_code == 200:
            self.logger.info(f'Response: {r.text}')
            return r.text
        else:
            return {'Error': r.status_code}

    
    def _send_set_command(self, cgi, parameter):
        if cgi == 'ptzautoframing.cgi':
            command = 'analytics'
        elif cgi == 'ptzautoframingexe.cgi':
            command = 'analytics'
        else:
            command = 'command'
        r = requests.get(f'http://{self._host_ip}/{command}/{cgi}', params=parameter, auth=self._digestauth, headers=self._headers)
        self.logger.info(f'Trying: {r.url}')
        self.logger.info(f'Status: {r.status_code}')
        
        if r.status_code == 204:
            return {
                'Status': r.status_code,
                'URL': r.url
                }
        else:
            return {'Error': r.status_code}
        

    def srg_start_autoframing(self):
        cgi = 'ptzautoframing.cgi'
        parameter = 'PtzAutoFraming=on'
        return self._send_set_command(cgi, parameter)

    def srg_stop_autoframing(self):
        cgi = 'ptzautoframing.cgi'
        parameter = 'PtzAutoFraming=off'
        return self._send_set_command(cgi, parameter)

    def srg_inq_autoframing(self, inq_parameter:str):
        cgi = 'inquiry.cgi'
        parameter = 'inq=PtzAutoFraming'
        inq_dict = inqanswer_to_dict(self._send_inq_command(cgi, parameter))
        if inq_parameter:
            if inq_parameter in inq_dict:
                return {inq_parameter: inq_dict[inq_parameter]}
        else:
            return inq_dict

    def srg_start_registeredfacetracking_autoframing(self):
        cgi = 'ptzautoframing.cgi'
        parameter = 'PtzAutoFramingRegisteredFaceTracking=on'
        return self._send_set_command(cgi, parameter)

    def srg_stop_registeredfacetracking_autoframing(self):
        cgi = 'ptzautoframing.cgi'
        parameter = 'PtzAutoFramingRegisteredFaceTracking=off'
        return self._send_set_command(cgi, parameter)

    def srg_multitrackingtargetnum(self, targets):
        response = {}
        cgi = 'ptzautoframing.cgi'
        if targets > 1:
            parameter = f'PtzAutoFramingMultiTrackingTargetNum={targets}'
            response['PtzAutoFramingMultiTrackingTargetNum'] = self._send_set_command(cgi, parameter)
            parameter = 'PtzAutoFramingMultiTrackingEnable=on'
        else:
            parameter = 'PtzAutoFramingMultiTrackingEnable=off'
        response['PtzAutoFramingMultiTrackingEnable'] = self._send_set_command(cgi, parameter)
        return response


    def srg_recall_preset(self, presetpos):
        cgi = 'presetposition.cgi'
        parameter = f'PresetCall={presetpos}'
        return self._send_set_command(cgi, parameter)
    
    def srg_inq_project(self):
        cgi = 'inquiry.cgi'
        parameter = 'inqjs=project'
        return self._send_inq_command(cgi, parameter)

    def srg_inq_system(self):
        cgi = 'inquiry.cgi'
        parameter = 'inqjs=system'
        return self._send_inq_command(cgi, parameter)


def main():
    camera = srg_cgi(host_ip='192.168.111.148', user='admin', password='Sony1234!')
    camera.srg_stop_autoframing()
    camera.srg_recall_preset(3)
    
    project = camera.srg_inq_project()

    print(f"Done with func: {project}")


if __name__ == "__main__":
    sys.path.append('/home/peter/source/rpi_zrct300_vlc/logger')
    print(sys.path)
    from logger import Logger

    main()
    print("Done")
else:
    from logger.logger import Logger