import sys
import logging
import json
import urllib.request

import websocket


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | [%(levelname)s] %(name)s ''%(funcName)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('/tmp/logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

min_lux_limit = 40
max_lux_limit = 500


def calc_cdm2_to_contrast_step_CH(candela: int):
    ## Define thresholds
    candela_min_step6 = 325
    candela_min_step5 = 250
    candela_min_step4 = 138
    candela_min_step3 = 70
    candela_min_step2 = 30
    candela_min_step1 = 14
    ## Define the scales
    if candela > candela_min_step6:
        max_contrast = 600
        max_candela = 1300
        min_candela = 325
        light_step = 6
    elif candela > candela_min_step5:
        max_contrast = 840
        max_candela = 1300
        min_candela = 250
        light_step = 5
    elif candela > candela_min_step4:
        max_contrast = 1000
        max_candela = 825
        min_candela = 138
        light_step = 4
    elif candela > candela_min_step3:
        max_contrast = 1000
        max_candela = 420
        min_candela = 70
        light_step = 3
    elif candela > candela_min_step2:
        max_contrast = 1000
        max_candela = 180
        min_candela = 30
        light_step = 2
    elif candela >= candela_min_step1:
        max_contrast = 1000
        max_candela = 81
        min_candela = 14
        light_step = 1

    ## The actual calculation
    tick = max_contrast / (max_candela - min_candela)
    contrast = int(tick * (candela - min_candela))
    logger.debug(f'"contrast": {contrast}, "step": {light_step}, "tick": {tick}, "candela": {candela}')
    return {"contrast": contrast, "step": light_step}

def calc_cdm2_to_contrast_step_BH(candela: int):
    ## Define thresholds
    candela_min_step6 = 425
    candela_min_step5 = 250
    candela_min_step4 = 138
    candela_min_step3 = 70
    candela_min_step2 = 30
    candela_min_step1 = 14
    ## Define the scales
    if candela > candela_min_step6:
        max_contrast = 600
        max_candela = 1700
        min_candela = 425
        light_step = 6
    elif candela > candela_min_step5:
        max_contrast = 1000
        max_candela = 1500
        min_candela = 250
        light_step = 5
    elif candela > candela_min_step4:
        max_contrast = 1000
        max_candela = 825
        min_candela = 138
        light_step = 4
    elif candela > candela_min_step3:
        max_contrast = 1000
        max_candela = 420
        min_candela = 70
        light_step = 3
    elif candela > candela_min_step2:
        max_contrast = 1000
        max_candela = 180
        min_candela = 30
        light_step = 2
    elif candela >= candela_min_step1:
        max_contrast = 1000
        max_candela = 81
        min_candela = 14
        light_step = 1

    ## The actual calculation
    tick = max_contrast / (max_candela - min_candela)
    contrast = int(tick * (candela - min_candela))
    return {"contrast": contrast, "step": light_step}


def lux_to_contrast_lightstep(cled_type: str, lux: int):
    ## Limit check
    if lux < min_lux_limit:
        lux = min_lux_limit
    if lux > max_lux_limit:
        lux = max_lux_limit
    
    ## Calc factor
    lux_scale = max_lux_limit - min_lux_limit
    try:
        lux_factor = lux_scale / (lux - min_lux_limit)
    except:
        lux_factor = 0
    if cled_type == "CH":
        max = 1300
        min = 14
        try:
            candela = (max / lux_factor) + min
        except:
            candela = min
        cdm2_dict = calc_cdm2_to_contrast_step_CH(candela=candela)
    if cled_type == "BH":
        max = 1700
        min = 14
        try:
            candela = (max / lux_factor) + min
        except:
            candela = min
        cdm2_dict = calc_cdm2_to_contrast_step_CH(candela=candela)


    url = f'http://127.0.0.1:5000/api/adcp/Contrast?contrast_value={cdm2_dict["contrast"]}&light_output_step={cdm2_dict["step"]}'
    logger.info(f"URL: {url}")
    r = urllib.request.urlopen(url)
    logger.info(f"Response: {r.msg}")

   


def on_message(wsapp, message):
    message = json.loads(message)
    if message["id"] == "3" and "state" in message.keys():
        logger.info(f"Lux: {message['state']['lux']} Level: {message['state']['lightlevel']}")
        lux_to_contrast_lightstep("CH", message['state']['lux'])
        

if __name__ == "__main__":
    logger.debug("Script started")
    ws_app = websocket.WebSocketApp('ws://localhost:443', on_message=on_message)
    ws_app.run_forever()
    logger.debug("Script ended")

