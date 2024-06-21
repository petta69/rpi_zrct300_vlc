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
from lib.camera import Camera

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
     Pause = "Pause"
     PlayDefaultPlaylist = "PlayDefaultPlaylist"
     PlayCustomPlaylist = "PlayCustomPlaylist"
     RestartVLC = "RestartVLC"

class ModelADCP(str, Enum):
     '''
     Valid functions for the ADCP class
     '''
     PowerOn = "PowerOn"
     PowerOff = "PowerOff"
     Preset1 = "Preset1"
     Preset2 = "Preset2"
     Preset3 = "Preset3"
     Preset4 = "Preset4"
     Preset5 = "Preset5"
     Preset6 = "Preset6"
     InputHDMI1 = "InputHDMI1"
     InputHDMI2 = "InputHDMI2"
     InputDP1 = "InputDP1"
     InputDP2 = "InputDP2"
     InputDP12 = "InputDP12"
     LightOutput1 = "LightOutput1"
     LightOutput2 = "LightOutput2"
     LightOutput3 = "LightOutput3"
     LightOutput4 = "LightOutput4"
     LightOutput5 = "LightOutput5"
     LightOutput6 = "LightOutput6"
     PictureMuteOn = "PictureMuteOn"
     PictureMuteOff = "PictureMuteOff"
     HDR = "HDR"
     SDR = "SDR"
     MotionFlowOff = "MotionFlowOff"
     MotionFlow1 = "MotionFlow1"
     MotionFlow2 = "MotionFlow2"
     MotionFlow3 = "MotionFlow3"
     MotionFlow4 = "MotionFlow4"
     WideModeNormal = "WideModeNormal"
     WideModeFull = "WideModeFull"
     WideModeZoom = "WideModeZoom"
     WideModeStretch = "WideModeStretch"
     WideModeNative = "WideModeNative"


class ModelVISCA(str, Enum):
    '''
    Valid functions for the visca class
    '''
    AutoFramingStart = "AutoFramingStart"
    AutoFramingStop = "AutoFramingStop"
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
    elif function is ModelVLC.Pause:
        vlc_player.pause()
    return {"Function": function} 

@app.get("/api/adcp/{function}")
async def adcp_api_function(function: ModelADCP):
    try:
        adcp_controller = adcp(host_ip=config.adcp_host, port=config.adcp_port, password=config.adcp_password, verbose=config.verbose)
    except:
        return {"ERROR": "Could not connect to host"}
    if function is ModelADCP.PowerOn:
        adcp_controller.send_power_on()
    elif function is ModelADCP.PowerOff:
        adcp_controller.send_power_off()
    elif function is ModelADCP.Preset1:
        adcp_controller.send_preset1()
    elif function is ModelADCP.Preset2:
        adcp_controller.send_preset2()
    elif function is ModelADCP.Preset3:
        adcp_controller.send_preset3()
    elif function is ModelADCP.Preset4:
        adcp_controller.send_preset4()
    elif function is ModelADCP.Preset5:
        adcp_controller.send_preset5()
    elif function is ModelADCP.Preset6:
        adcp_controller.send_preset6()
    elif function is ModelADCP.LightOutput1:
        adcp_controller.send_lightoutput1()
    elif function is ModelADCP.LightOutput2:
        adcp_controller.send_lightoutput2()
    elif function is ModelADCP.LightOutput3:
        adcp_controller.send_lightoutput3()
    elif function is ModelADCP.LightOutput4:
        adcp_controller.send_lightoutput4()
    elif function is ModelADCP.LightOutput5:
        adcp_controller.send_lightoutput5()
    elif function is ModelADCP.LightOutput6:
        adcp_controller.send_lightoutput6()
    elif function is ModelADCP.InputDP1:
        adcp_controller.send_inputDP1()
    elif function is ModelADCP.InputDP2:
        adcp_controller.send_inputDP2()
    elif function is ModelADCP.InputDP12:
        adcp_controller.send_inputDP12()
    elif function is ModelADCP.InputHDMI1:
        adcp_controller.send_inputHDMI1()
    elif function is ModelADCP.InputHDMI2:
        adcp_controller.send_inputHDMI2()
    elif function is ModelADCP.PictureMuteOn:
        adcp_controller.send_PictureMuteOn()
    elif function is ModelADCP.PictureMuteOff:
        adcp_controller.send_PictureMuteOff()
    elif function is ModelADCP.HDR:
        adcp_controller.send_HDR()
    elif function is ModelADCP.MotionFlowOff:
        adcp_controller.send_MotionFlowOff()
    elif function is ModelADCP.MotionFlow1:
        adcp_controller.send_MotionFlow1()
    elif function is ModelADCP.MotionFlow2:
        adcp_controller.send_MotionFlow2()
    elif function is ModelADCP.MotionFlow3:
        adcp_controller.send_MotionFlow3()
    elif function is ModelADCP.MotionFlow4:
        adcp_controller.send_MotionFlow4()
    elif function is ModelADCP.WideModeNormal:
        adcp_controller.send_WideModeNormal()
    elif function is ModelADCP.WideModeFull:
        adcp_controller.send_WideModeFull()
    elif function is ModelADCP.WideModeZoom:
        adcp_controller.send_WideModeZoom()
    elif function is ModelADCP.WideModeStretch:
        adcp_controller.send_WideModeStretch()
    elif function is ModelADCP.WideModeNative:
        adcp_controller.send_WideModeNative()
    return {"Function": function}

@app.get("/api/visca/{function}")
async def visca_api_function(function: ModelVISCA):
    try:
        visca_controller = Camera(ip=config.visca_host, port=config.visca_port, verbose=config.verbose)
    except:
        return {"ERROR": "Could not connect to host"}
    if function is ModelVISCA.AutoFramingStart:
        visca_controller.autoframing_start()
    elif function is ModelVISCA.AutoFramingStop:
        visca_controller.autoframing_stop()
    elif function is ModelVISCA.Preset1:
        visca_controller.recall_preset1()
    elif function is ModelVISCA.Preset2:
        visca_controller.recall_preset2()
    elif function is ModelVISCA.Preset3:
        visca_controller.recall_preset3()
    elif function is ModelVISCA.Preset4:
        visca_controller.recall_preset4()
    elif function is ModelVISCA.Preset5:
        visca_controller.recall_preset5()
    elif function is ModelVISCA.Preset6:
        visca_controller.recall_preset6()







## TemplateResponse
@app.get("/vlc", response_class=HTMLResponse)
async def vlc(request: Request):
    return templates.TemplateResponse(
        request=request, name="vlc.html"
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