#!/bin/python3

import sys
import os
import timeit

from enum import Enum
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

## Get settings and store in dict
from settings import ReadConfig, ModelConfig, SaveConfig
config = ReadConfig()

## Configure logger object
from logger.logger import Logger
logger = Logger(name=__name__, level=config.verbose, file_path="/tmp/rpi_zrct300_vlc.txt").get_logger()

from lib.crontab_settings import write_crontab, read_crontab, remove_crontab
from lib.video_player import player
from lib.start_vlc import restart_vlc, start_vlc
from lib.adcp import adcp
from lib.camera import Camera
from lib.srg_cgi import srg_cgi
from lib.system import reboot_rpi

current_user = os.getlogin()
schedule = read_crontab(current_user)

app = FastAPI(title="RPI5 Control")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="templates")


flood_oldfunction = "none"
flood_oldtime = timeit.default_timer()

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
     PlayDesignPlaylist = "PlayDesignPlaylist"
     PlayCorporatePlaylist = "PlayCorporatePlaylist"
     PlayRetailPlaylist = "PlayRetailPlaylist"
     PlayCustomPlaylist = "PlayCustomPlaylist"
     RestartVLC = "RestartVLC"
     Info = "Info"
     Status = "Status"
     Get_Title = "Get_Title"

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
     HDRAuto = "HDRAuto"
     MotionFlowOff = "MotionFlowOff"
     MotionFlow1 = "MotionFlow1"
     MotionFlow2 = "MotionFlow2"
     MotionFlow3 = "MotionFlow3"
     MotionFlow4 = "MotionFlow4"
     RealityCreationOn = "RealityCreationOn"
     RealityCreationOff = "RealityCreationOff"
     WideModeNormal = "WideModeNormal"
     WideModeFull = "WideModeFull"
     WideModeZoom = "WideModeZoom"
     WideModeStretch = "WideModeStretch"
     WideModeNative = "WideModeNative"
     Status = "Status"
     Contrast = "Contrast"


class ModelSRGCGI(str, Enum):
    '''
    Valid functions for the visca class
    '''
    AutoFramingStart = "AutoFramingStart"
    AutoFramingStop = "AutoFramingStop"
    AutoFraming = "AutoFraming"
    Preset1 = "Preset1"
    Preset2 = "Preset2"
    Preset3 = "Preset3"
    Preset4 = "Preset4"
    Preset5 = "Preset5"
    Preset6 = "Preset6"
    System = "System"
    RegisteredFaceTrackingStart = "RegisteredFaceTrackingStart"
    RegisteredFaceTrackingStop = "RegisteredFaceTrackingStop"
    MultiTrackinTargetNum1 = "MultiTrackinTargetNum1"
    MultiTrackinTargetNum2 = "MultiTrackinTargetNum2"
    MultiTrackinTargetNum3 = "MultiTrackinTargetNum3"
    MultiTrackinTargetNum4 = "MultiTrackinTargetNum4"

class ModelSystem(str, Enum):
    '''
    Valid functions for the system class
    '''
    Restart = "Restart"

def check_flooding(flood_function, flood_timeout=5):
    global flood_oldfunction
    global flood_oldtime
    now = timeit.default_timer()
    if flood_function == flood_oldfunction:
        if now - flood_oldtime < flood_timeout:
            flood_oldtime = now
            return True
        else:
            flood_oldtime = now
            return False
    else:
        flood_oldfunction = flood_function
        flood_oldtime = now
        return False
    


## API calls
@app.get("/api/vlc/{function}")
async def vlc_api_function(function: ModelVLC):
    if check_flooding(function.value, flood_timeout=1):
        return {'Error': 'Flooding'}
    try:
        config = ReadConfig()
        vlc_player = player()
    except:
        start_vlc()
        vlc_player = player()
    if function is ModelVLC.PlayDefaultPlaylist:
        restart_vlc()
        playlist = vlc_player.play_default_list(config.vlc_default_videodir)
        return {"Playlist": playlist}
    elif function is ModelVLC.PlayDesignPlaylist:
        restart_vlc()
        playlist = vlc_player.play_design_list(config.vlc_default_videodir)
        return {"Playlist": playlist}
    elif function is ModelVLC.PlayCorporatePlaylist:
        restart_vlc()
        playlist = vlc_player.play_corporate_list(config.vlc_default_videodir)
        return {"Playlist": playlist}
    elif function is ModelVLC.PlayRetailPlaylist:
        restart_vlc()
        playlist = vlc_player.play_retail_list(config.vlc_default_videodir)
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
    elif function is ModelVLC.Info:
        return vlc_player.info()
    elif function is ModelVLC.Status:
        return vlc_player.status()
    return {"Function": function} 

@app.get("/api/adcp/{function}")
async def adcp_api_function(function: ModelADCP, contrast_value: int = 0, light_output_step: int = 0):
    result = []
    ## Check flooding. NOTE: If we send contrast_value and light_output_step it means it comes from deconz and flooding is allowed
    if check_flooding(function.value) and contrast_value == 0 and light_output_step == 0:
        return {'Error': 'Flooding'}
    try:
        config = ReadConfig()
        adcp_controller = adcp(host_ip=config.adcp_host, port=config.adcp_port, password=config.adcp_password, verbose=config.verbose)
    except:
        return {"ERROR": "Could not connect to host"}
    if function is ModelADCP.PowerOn:
        result.append(adcp_controller.send_power_on())
    elif function is ModelADCP.PowerOff:
        result.append(adcp_controller.send_power_off())
    elif function is ModelADCP.Preset1:
        result.append(adcp_controller.send_preset1())
    elif function is ModelADCP.Preset2:
        result.append(adcp_controller.send_preset2())
    elif function is ModelADCP.Preset3:
        result.append(adcp_controller.send_preset3())
    elif function is ModelADCP.Preset4:
        result.append(adcp_controller.send_preset4())
    elif function is ModelADCP.Preset5:
        result.append(adcp_controller.send_preset5())
    elif function is ModelADCP.Preset6:
        result.append(adcp_controller.send_preset6())
    elif function is ModelADCP.LightOutput1:
        result.append(adcp_controller.send_lightoutput1())
    elif function is ModelADCP.LightOutput2:
        result.append(adcp_controller.send_lightoutput2())
    elif function is ModelADCP.LightOutput3:
        result.append(adcp_controller.send_lightoutput3())
    elif function is ModelADCP.LightOutput4:
        result.append(adcp_controller.send_lightoutput4())
    elif function is ModelADCP.LightOutput5:
        result.append(adcp_controller.send_lightoutput5())
    elif function is ModelADCP.LightOutput6:
        result.append(adcp_controller.send_lightoutput6())
    elif function is ModelADCP.InputDP1:
        result.append(adcp_controller.send_inputDP1())
    elif function is ModelADCP.InputDP2:
        result.append(adcp_controller.send_inputDP2())
    elif function is ModelADCP.InputDP12:
        result.append(adcp_controller.send_inputDP12())
    elif function is ModelADCP.InputHDMI1:
        result.append(adcp_controller.send_inputHDMI1())
    elif function is ModelADCP.InputHDMI2:
        result.append(adcp_controller.send_inputHDMI2())
    elif function is ModelADCP.PictureMuteOn:
        result.append(adcp_controller.send_PictureMuteOn())
    elif function is ModelADCP.PictureMuteOff:
        result.append(adcp_controller.send_PictureMuteOff())
    elif function is ModelADCP.SDR:
        result.append(adcp_controller.send_SDR())
    elif function is ModelADCP.HDR:
        result.append(adcp_controller.send_HDR())
    elif function is ModelADCP.HDRAuto:
        result.append(adcp_controller.send_HDR_Auto())
    elif function is ModelADCP.RealityCreationOn:
        result.append(adcp_controller.send_RealitycreationOn())
    elif function is ModelADCP.RealityCreationOff:
        result.append(adcp_controller.send_RealityCreationOff())
    elif function is ModelADCP.MotionFlowOff:
        result.append(adcp_controller.send_MotionFlowOff())
    elif function is ModelADCP.MotionFlow1:
        result.append(adcp_controller.send_MotionFlow1())
    elif function is ModelADCP.MotionFlow2:
        result.append(adcp_controller.send_MotionFlow2())
    elif function is ModelADCP.MotionFlow3:
        result.append(adcp_controller.send_MotionFlow3())
    elif function is ModelADCP.MotionFlow4:
        result.append(adcp_controller.send_MotionFlow4())
    elif function is ModelADCP.WideModeNormal:
        result.append(adcp_controller.send_WideModeNormal())
    elif function is ModelADCP.WideModeFull:
        result.append(adcp_controller.send_WideModeFull())
    elif function is ModelADCP.WideModeZoom:
        result.append(adcp_controller.send_WideModeZoom())
    elif function is ModelADCP.WideModeStretch:
        result.append(adcp_controller.send_WideModeStretch())
    elif function is ModelADCP.WideModeNative:
        result.append(adcp_controller.send_WideModeNative())
    elif function is ModelADCP.Status:
        ## This function returns a list
        response = adcp_controller.send_Status()
        for item in response:
            result.append(item)
    elif function is ModelADCP.Contrast:
        logger.debug(f"New contrast: {contrast_value} -- LightOutputStep: {light_output_step}")
        result.append(adcp_controller.send_LightSensorUpdate(contrast_value=contrast_value, light_output_step=light_output_step))
    logger.debug(f'result: {result}')
    return result

@app.get("/api/srgcgi/{function}")
async def srgcgi_api_function(function: ModelSRGCGI):
    result = []
    if check_flooding(function.value):
        return {'Error': 'Flooding'}
    try:
        config = ReadConfig()
        srgcgi_controller = srg_cgi(user=config.srgcgi_username, password=config.srgcgi_password, host_ip=config.srgcgi_host, port=config.srgcgi_port, verbose=config.verbose)
    except:
        return {"ERROR": "Could not connect to host"}
    if function is ModelSRGCGI.AutoFramingStart:
        result.append(srgcgi_controller.srg_start_autoframing())
    elif function is ModelSRGCGI.AutoFramingStop:
        result.append(srgcgi_controller.srg_stop_autoframing())
    elif function is ModelSRGCGI.Preset1:
        result.append(srgcgi_controller.srg_stop_autoframing())
        result.append(srgcgi_controller.srg_recall_preset(presetpos=1))
    elif function is ModelSRGCGI.Preset2:
        result.append(srgcgi_controller.srg_stop_autoframing())
        result.append(srgcgi_controller.srg_recall_preset(presetpos=2))
    elif function is ModelSRGCGI.Preset3:
        result.append(srgcgi_controller.srg_stop_autoframing())
        result.append(srgcgi_controller.srg_recall_preset(presetpos=3))
    elif function is ModelSRGCGI.Preset4:
        result.append(srgcgi_controller.srg_stop_autoframing())
        result.append(srgcgi_controller.srg_recall_preset(presetpos=4))
    elif function is ModelSRGCGI.Preset5:
        result.append(srgcgi_controller.srg_stop_autoframing())
        result.append(srgcgi_controller.srg_recall_preset(presetpos=5))
    elif function is ModelSRGCGI.Preset6:
        result.append(srgcgi_controller.srg_stop_autoframing())
        result.append(srgcgi_controller.srg_recall_preset(presetpos=6))
    elif function is ModelSRGCGI.System:
        result.append(srgcgi_controller.srg_inq_system())
    elif function is ModelSRGCGI.RegisteredFaceTrackingStart:
        autoframing = srgcgi_controller.srg_inq_autoframing('PtzAutoFraming')
        if 'PtzAutoFraming' in autoframing:
            if autoframing['PtzAutoFraming'] == "on":
                result.append(srgcgi_controller.srg_stop_autoframing())        
                result.append(srgcgi_controller.srg_start_registeredfacetracking_autoframing())
                result.append(srgcgi_controller.srg_start_autoframing())
            else:
                result.append(srgcgi_controller.srg_start_registeredfacetracking_autoframing())
        else:
            result.append(srgcgi_controller.srg_start_registeredfacetracking_autoframing())
    elif function is ModelSRGCGI.RegisteredFaceTrackingStop:
        autoframing = srgcgi_controller.srg_inq_autoframing('PtzAutoFraming')
        if 'PtzAutoFraming' in autoframing:
            if autoframing['PtzAutoFraming'] == "on":
                result.append(srgcgi_controller.srg_stop_autoframing())        
                result.append(srgcgi_controller.srg_stop_registeredfacetracking_autoframing())
                result.append(srgcgi_controller.srg_start_autoframing())
            else:
                result.append(srgcgi_controller.srg_stop_registeredfacetracking_autoframing())
        else:
            result.append(srgcgi_controller.srg_stop_registeredfacetracking_autoframing())
    elif function is ModelSRGCGI.MultiTrackinTargetNum1:
        result.append(srgcgi_controller.srg_multitrackingtargetnum(1))
    elif function is ModelSRGCGI.MultiTrackinTargetNum2:
        result.append(srgcgi_controller.srg_multitrackingtargetnum(2))
    elif function is ModelSRGCGI.MultiTrackinTargetNum3:
        result.append(srgcgi_controller.srg_multitrackingtargetnum(3))
    elif function is ModelSRGCGI.MultiTrackinTargetNum4:
        result.append(srgcgi_controller.srg_multitrackingtargetnum(4))
    return result


@app.get("/api/system/{function}")
async def system_api_function(function: ModelSystem):
    if function is ModelSystem.Restart:
        if check_flooding(function.value):
            return {'Error': 'Flooding'}
        ## Rebooting PI5
        reboot_rpi()






## TemplateResponse
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    config = ReadConfig()
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/vlc", response_class=HTMLResponse)
async def vlc(request: Request, function: ModelVLC | None=None):
    ## If we get a function we need to execute that action. Result is used to print status.
    config = ReadConfig()
    context = {}
    if function:
        try:
            result = await vlc_api_function(function)
            ## Create context to pass to bootstrap
            if function is ModelVLC.Status:
                context["status"] = result
            elif function is ModelVLC.Info:
                context["info"] = result
            else:
                context["function"] = result
        except:
            context["status"] = {"Error connecting to VLC"}

    return templates.TemplateResponse(
        request=request, name="vlc.html", context=context
    )

@app.get("/zrct300", response_class=HTMLResponse)
async def zrct300(request: Request, function: ModelADCP | None=None):
    ## If we get a function we need to execute that action. Result is used to print status.
    config = ReadConfig()
    context = {}
    if function:
        result = await adcp_api_function(function)
        ## Create context to pass to bootstrap
        context["status"] = result

    return templates.TemplateResponse(
        request=request, name="zrct300.html", context=context
    )

@app.get("/srg", response_class=HTMLResponse)
async def srg(request: Request, function: ModelSRGCGI | None=None):
    ## If we get a function we need to execute that action. Result is used to print status.
    config = ReadConfig()
    context = {}
    if function:
        result = await srgcgi_api_function(function)
        ## Create context to pass to bootstrap
        context["status"] = result

    return templates.TemplateResponse(
        request=request, name="srg.html", context=context
    )

@app.get('/settings', response_class=HTMLResponse)
async def settings(request: Request):
    ## Uses settings.json to print all valid keys and values
    config = ReadConfig()
    settings = {}
    context = {}
    for k,v in iter(config):
        ## Transcode BaseModel object to dict
        print(f"{k} -> {v}")
        settings[k] = v
    context['config'] = settings
    ## Read schedule
    cron_read = read_crontab(cron_user=current_user)
    context['config'].update(cron_read)
    return templates.TemplateResponse(
        request=request, name="settings.html", context=context
    )

@app.post('/settings')
async def settings_update(request: Request, 
                          vlc_default_videodir: str = Form(config.vlc_default_videodir),
                          vlc_custom_usb_videodir: str = Form(config.vlc_custom_usb_videodir),
                          adcp_host: str = Form(config.adcp_host),
                          adcp_port: int = Form(config.adcp_port),
                          adcp_password: str = Form(config.adcp_password),
                          adcp_use_schedule: bool = Form(False),
                          srgcgi_host: str = Form(config.srgcgi_host),
                          srgcgi_port: int = Form(config.srgcgi_port),
                          srgcgi_username: str = Form(config.srgcgi_username),
                          srgcgi_password: str = Form(config.srgcgi_password),
                          deconz_min_lux: str = Form(config.deconz_min_lux),
                          deconz_max_lux: str = Form(config.deconz_max_lux),
                          deconz_cled_type: str = Form(config.deconz_cled_type),
                          verbose: int = Form(config.verbose),
                          monday_active: bool = Form(False),
                          tuesday_active: bool = Form(False),
                          wednesday_active: bool = Form(False),
                          thursday_active: bool = Form(False),
                          friday_active: bool = Form(False),
                          saturday_active: bool = Form(False),
                          sunday_active: bool = Form(False),
                          monday_on: str = Form(...),
                          monday_off: str = Form(...),
                          tuesday_on: str = Form(...),
                          tuesday_off: str = Form(...),
                          wednesday_on: str = Form(...),
                          wednesday_off: str = Form(...),
                          thursday_on: str = Form(...),
                          thursday_off: str = Form(...),
                          friday_on: str = Form(...),
                          friday_off: str = Form(...),
                          saturday_on: str = Form(...),
                          saturday_off: str = Form(...),
                          sunday_on: str = Form(...),
                          sunday_off: str = Form(...)
                          ):
        
    ## Process for crontab
    if adcp_use_schedule:
        settings_cron = {
            'monday_active': monday_active,
            'monday_on': monday_on,
            'monday_off': monday_off,
            'tuesday_active': tuesday_active,
            'tuesday_on': tuesday_on,
            'tuesday_off': tuesday_off,
            'wednesday_active': wednesday_active,
            'wednesday_on': wednesday_on,
            'wednesday_off': wednesday_off,
            'thursday_active': thursday_active,
            'thursday_on': thursday_on,
            'thursday_off': thursday_off,
            'friday_active': friday_active,
            'friday_on': friday_on,
            'friday_off': friday_off,
            'saturday_active': saturday_active,
            'saturday_on': saturday_on,
            'saturday_off': saturday_off,
            'sunday_active': sunday_active,
            'sunday_on': sunday_on,
            'sunday_off': sunday_off
        }
        remove_crontab(cron_user=current_user)
        write_crontab(cron_user=current_user, cron_dict=settings_cron)
    else:
        remove_crontab(cron_user=current_user)

    ## After pressing submit we need to save dict to settings.json
    data = {
        'vlc_default_videodir': vlc_default_videodir,
        'vlc_custom_usb_videodir': vlc_custom_usb_videodir,
        'adcp_host': adcp_host,
        'adcp_port': adcp_port,
        'adcp_password': adcp_password,
        'adcp_use_schedule': adcp_use_schedule,
        'srgcgi_host': srgcgi_host,
        'srgcgi_port': srgcgi_port,
        'srgcgi_username': srgcgi_username,
        'srgcgi_password': srgcgi_password,
        'deconz_min_lux': deconz_min_lux,
        'deconz_max_lux': deconz_max_lux,
        'deconz_cled_type': deconz_cled_type,
        'verbose': verbose
    }
    data_config = ModelConfig(**data)
    ## This save also read out the updated config
    config = SaveConfig(data_config)

    settings = {}
    context = {}
    for k,v in iter(config):
        ## Transcode BaseModel object to dict
        print(f"{k} -> {v}")
        settings[k] = v
    context['config'] = settings
    cron_read = read_crontab(cron_user=current_user)
    context['config'].update(cron_read)

    return templates.TemplateResponse(
        request=request, name="settings.html", context=context
    )



if(__name__) == '__main__':
        import uvicorn
        uvicorn.run(
        "main:app",
        host    = "0.0.0.0",
        port    = 5000, 
        reload  = True
    )