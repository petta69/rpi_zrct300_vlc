import json
import os
from typing import Optional
from pydantic import BaseModel
       
##
## Module for reading settings.json file into a config object
##


class ModelConfig(BaseModel):
    vlc_default_videodir: Optional[str] = f"{os.environ['HOME']}/Videos"
    vlc_custom_usb_videodir: Optional[str] = "media"
    adcp_host: Optional[str] = "192.168.0.10"
    adcp_port: Optional[int] = 53595
    adcp_password: Optional[str] = "chiron01"
    visca_host: Optional[str] = "192.168.0.20"
    visca_port: Optional[int] = 52381
    verbose: Optional[int] = 5

class ReadSettings():
    ### Class for reading settings.json
    def __init__(self):
        self.filename = "settings.json"
    
    def read_data(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return ModelConfig(**data)
        except FileNotFoundError:
            print(f"ERROR: File not found: {self.filename}")
            return False
        

def ReadConfig():
    reader = ReadSettings()
    return reader.read_data()

if __name__ == "__main__":
    conf = ReadConfig()
    print(conf)