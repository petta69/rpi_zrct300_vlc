#!/bin/python3

import sys
import os

from enum import Enum
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from settings import ReadConfig
from lib.video_player import player
from lib.start_vlc import restart_vlc, start_vlc
from lib.adcp import adcp

config = ReadConfig()

app = FastAPI(title="RPI5 Control")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ModelVLC(str, Enum):
     '''
     Valid functions for the VLC class
     '''
     Play = "Play"
     Stop = "Stop"
     Next = "Next"
     Prev = "Prev"
     PlayDefaultPlaylist = "PlayDefaultPlaylist"
     PlayCustomPlaylist = "PlayCustomPlaylist"
     RestartVLC = "RestartVLC"

class ModelADCP(str, Enum):
     '''
     Valid functions for the VLC class
     '''
     PowerOn = "PowerOn"
     PowerOff = "PowerOff"
     Preset1 = "Preset1"
     Preset2 = "Preset2"
     Preset3 = "Preset3"
     Preset4 = "Preset4"
     Preset5 = "Preset5"
     Preset6 = "Preset6"

## API calls
@app.get("/api/vlc/{function}")
async def vlc_api_function(function: ModelVLC):
    try:
        vlc_player = player()
    except:
        start_vlc()
        vlc_player = player()
    if function is ModelVLC.PlayDefaultPlaylist:
        restart_vlc()
        playlist = vlc_player.play_default_list(config.vlc_default_videodir)
        return {"Playlist": playlist}
    elif function is ModelVLC.PlayCustomPlaylist:
        restart_vlc()
        playlist = vlc_player.play_custom_list(config.vlc_custom_usb_videodir)
        return {"Playlist": playlist}
    elif function is ModelVLC.Next:
        vlc_player.next()
    elif function is ModelVLC.Prev:
        vlc_player.prev()
    elif function is ModelVLC.RestartVLC:
        restart_vlc()
    return {"Function": function} 

@app.get("/api/adcp/{function}")
async def zrct_api_function(function: ModelADCP):
    try:
        adcp_controller = adcp()
    except:
        return {"ERROR": "Could not connect to host"}
    if function is ModelADCP.PowerOn:
        adcp_controller.send_power_on()
    return {"Function": function}


## TemplateResponse
@app.get("/vlc", response_class=HTMLResponse)
async def vlc(request: Request, function: str):
    return templates.TemplateResponse(
        {"request": request, "function": function}, name="vlc.html"
    )

@app.get("/zrct300", response_class=HTMLResponse)
async def zrct300(request: Request):
    return templates.TemplateResponse(
        request=request, name="zrct300.html"
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


if(__name__) == '__main__':
        import uvicorn
        uvicorn.run(
        "main:app",
        host    = "0.0.0.0",
        port    = 5000, 
        reload  = True
    )