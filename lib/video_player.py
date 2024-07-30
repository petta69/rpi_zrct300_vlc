import sys
import os

import socket
from logger.logger import Logger

verbose = 5
logger = Logger(name=__name__, level=verbose).get_logger()

class playlist():
    def __init__(self):
        pass

class player():
    def __init__(self):
        self.SEEK_TIME = 20
        self.MAX_VOL = 512
        self.MIN_VOL = 0
        self.DEFAULT_VOL = 256
        self.VOL_STEP = 13
        self.current_vol = self.DEFAULT_VOL


    def play_default_list(self, media_dir):
        self.media_dir = media_dir
        self.req("clear") ## Clears the playlist
        self.req("loop on")
        self.req("random on")
        self.req(f"add {self.media_dir}")
        print(f"Start Playing from: {self.media_dir}")
        return self.media_dir
    
    def play_design_list(self, media_dir):
        self.media_dir = media_dir
        self.media_playlist = f'{self.media_dir}/design.m3u'
        if os.path.isfile(self.media_playlist):
            self.req("clear") ## Clears the playlist
            self.req("loop on")
            self.req("random on")
            self.req(f"add {self.media_playlist}")
            print(f"Start Playing: {self.media_playlist}")
            return self.media_playlist
        else:
            return "Error: Design directory does not exist"
    
    def play_corporate_list(self, media_dir):
        self.media_dir = media_dir
        self.media_playlist = f'{self.media_dir}/corporate.m3u'
        if os.path.isfile(self.media_playlist):
            self.req("clear") ## Clears the playlist
            self.req("loop on")
            self.req("random on")
            self.req(f"add {self.media_playlist}")
            print(f"Start Playing: {self.media_playlist}")
            return self.media_playlist
        else:
            return "Error: Corporate directory does not exist"
    
    def play_retail_list(self, media_dir):
        self.media_dir = media_dir
        self.media_playlist = f'{self.media_dir}/retail.m3u'
        if os.path.isfile(self.media_playlist):
            self.req("clear") ## Clears the playlist
            self.req("loop on")
            self.req("random on")
            self.req(f"add {self.media_playlist}")
            print(f"Start Playing: {self.media_playlist}")
            return self.media_playlist
        else:
            return "Error: Retail directory does not exist"

    def play_custom_list(self, custom_dirname):
        custom_dirname = custom_dirname
        self.req("clear") ## Clears the playlist
        self.req("loop on")
        self.req("random on")
        self.media_dir = find_usb_media_dir(custom_dirname)
        self.req(f"add {self.media_dir}")
        print(f"Start Playing from: {self.media_dir}")
        return self.media_dir


    def next(self):
        self.req("next")
        print("Next")
        pass

    def prev(self):
        self.req("prev")
        print("Previous")
        pass

    def play(self):
        self.req("play")
        print("Play")
        pass

    def pause(self):
        self.req("pause")
        print("Pause")
        pass

    def help(self):
        response = self.req("help")
        print("Help")
        print(response)
        return response

    def info(self) -> list:
        response = self.req("info")
        print("Info")
        print(response)
        return response

    def get_title(self) -> str:
        response = self.req("get_title")[0]
        response = response.lstrip('> ')
        print(response)
        return response

    def playlist(self) -> list:
        response = self.req("playlist")
        response[0] = response[0].lstrip('> ')
        print(response)
        return response


    def status(self) -> list:
        response = self.req("status")
        response[0] = response[0].lstrip('> ')
        print("Status")
        print(response)
        return response


    def volup(self):
        self.current_vol = self.current_vol + self.VOL_STEP
        self.req("volume " + str(self.current_vol))
        print("Volume up")
        pass

    def voldown(self):
        self.current_vol = self.current_vol - self.VOL_STEP
        self.req("volume " + str(self.current_vol))
        print("Volume Down")
        pass

    def seek(self, forward: bool):
        length = self._timeinfo("get_length")
        print(length)
        cur = self._timeinfo("get_time")
        print(cur)
        if (forward):
            seekable = cur + self.SEEK_TIME
        else:
            seekable = cur - self.SEEK_TIME
        if seekable > length:
            seekable = length - 5
        if seekable < 0:
            seekable = 0
        self.req("seek " + str(seekable))
        print("Seek: ",seekable," Cur: ",cur,"Len: ",length)
        pass

    def _timeinfo(self, msg):
        length = self.req(msg, True).split("\r\n")
        if (len(length) < 2):
            return None
        length = length[1].split(" ")
        if (len(length) < 2):
            return None
        try:
            num = int(length[1])
            return num
        except:
            return None

    def req(self, msg: str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data
                sock.settimeout(0.5)
                sock.connect(('127.0.0.1', 44500))
                response = ""
                received = ""
                sock.sendall(bytes(msg + '\n', "utf-8"))
                # if True:
                try:
                    while (True):
                        received = (sock.recv(4096)).decode()
                        response = response + received
                        
                        if response.count("\r\n") > 1:
                            sock.close()
                            break
                except:
                    response = response + received
                    pass
                sock.close()
                response_list = response.splitlines()
                # # Remove VLC welcome text
                del response_list[:2]
                print(response_list)
                return response_list
        except:
            return None

 
def find_usb_media_dir(custom_usb_videodir, mindepth=2, maxdepth=3):
    start_dir = '/media'
    depth = 0
    for root, dirs, files in os.walk(start_dir):
        depth = depth + 1
        if depth >= mindepth and depth <= maxdepth and custom_usb_videodir in dirs:
            if os.path.isdir(f"{root}/{custom_usb_videodir}"):
                print(f"INFO: Directories in path - {root} -- {dirs}")
                return f"{root}/{custom_usb_videodir}"
    ## If we do not find dir we return False
    return False        


if __name__ == "__main__":

    #'vlc --intf rc --rc-host 127.0.0.1:44500'
    Player=player()
    Player.status()


    
        
        
