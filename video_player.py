import sys
import os
import time
import string

import socket
from threading import Thread 

class playlist():
    def __init__(self):
        pass


class player():
    def __init__(self):
        self.is_initiated = False
        self.SEEK_TIME = 20
        self.MAX_VOL = 512
        self.MIN_VOL = 0
        self.DEFAULT_VOL = 256
        self.VOL_STEP = 13
        self.current_vol = self.DEFAULT_VOL
        if self.is_playing():
            self.is_initiated = True

    def play_default_list(self):
        self.is_initiated = True
        self.thrededreq("loop on")
        #self.thrededreq("random on")
        self.thrededreq("add /home/peter/Videos/qwe.m3u")
        print("Start Playing")

    def is_playing(self) -> bool:
        response = self.req("is_playing")[0]
        response = response.lstrip('> ')
        if response == '1':
            return True
        else:
            return False


    def next(self):
        if not self.is_initiated:
            self.toggle_play()
            return
        self.thrededreq("next")
        print("Next")
        pass

    def prev(self):
        if not self.is_initiated:
            self.toggle_play()
            return
        self.thrededreq("prev")
        print("Previous")
        pass

    def play(self):
        self.thrededreq("play")
        print("Play")
        pass

    def pause(self):
        if not self.is_initiated:
            self.toggle_play()
            return
        self.thrededreq("pause")
        print("Pause")
        pass

    def help(self):
        if not self.is_initiated:
            self.toggle_play()
            return
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
        self.thrededreq("volume " + str(self.current_vol))
        print("Volume up")
        pass

    def voldown(self):
        self.current_vol = self.current_vol - self.VOL_STEP
        self.thrededreq("volume " + str(self.current_vol))
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
        self.thrededreq("seek " + str(seekable))
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
            pass

    def thrededreq(self, msg):
        Thread(target=self.req, args=(msg,)).start()


    
            
        
if __name__ == "__main__":

    #'vlc --intf rc --rc-host 127.0.0.1:44500'
    Player=player()
    Player.status()


    
        
        