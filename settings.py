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
    adcp_host: Optional[str] = "192.168.6.10"
    adcp_port: Optional[int] = 53595
    adcp_password: Optional[str] = "chiron01"
    adcp_use_schedule: Optional[bool] = False
    # visca_host: Optional[str] = "192.168.0.20"
    # visca_port: Optional[int] = 52381
    srgcgi_host: Optional[str] = ""
    srgcgi_port: Optional[int] = 80
    srgcgi_username: Optional[str] = "admin"
    srgcgi_password: Optional[str] = "1234"
    deconz_active: Optional[bool] = False
    deconz_min_lux: Optional[int] = 40
    deconz_max_lux: Optional[int] = 500
    deconz_cled_type: Optional[str] = "CH"
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
    
    def save_data(self, config):
        try:
            with open(self.filename, "+w") as outfile:
                data = {}
                for k,v in iter(config):
                    ## Transcode BaseModel object to dict
                    print(f"{k} -> {v}")
                    data[k] = v
                json.dump(data, outfile, indent=4)
                return ModelConfig(**data)
        except FileNotFoundError:
            print(f"ERROR: File not found: {self.filename}")
            return False

def ReadConfig():
    reader = ReadSettings()
    return reader.read_data()

def SaveConfig(config):
    reader = ReadSettings()
    reader.save_data(config=config)
    return reader.read_data()

if __name__ == "__main__":
    conf = ReadConfig()
    print(conf)