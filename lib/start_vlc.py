import subprocess
import os
import time
from logger.logger import Logger

verbose = 5
vlc_cmd='/usr/bin/cvlc -f --intf rc --x11-display :0 -A alsa --alsa-audio-channels 6 --drm-vout-source-modeset --drm-vout-display HDMI-A-1 --no-video-title-show --no-osd --no-spu --rc-host 127.0.0.1:44500'

def process_exists(proc_name):
    # # Use pgrep in order to find any existing VLC process
    pgrep = subprocess.Popen(['pgrep', proc_name], stdout=subprocess.PIPE)
    output = pgrep.stdout.read().decode('utf-8')
    pgrep.stdout.close()
    pgrep.wait()

    #logger.debug(f"Found pid's: {output}")
    vlc_procs = []
    for line in output.split("\n"):
        if line:
            vlc_procs.append(line)
    # # Return a list of all VLC pid's
    return vlc_procs

def kill_vlc_procs(pid):
    # # Kill given VLC process
    try:
        subprocess.Popen(['kill', '-10', pid])
    except:
        logger.error(f"Could not kill proc: {pid}")
        return False
    return True


def start_vlc() -> bool:
    """ Start CVLC in background and make ready for remote control
        First we make sure to add correct screen"""
    os.environ['DISPLAY'] = ":0"
    my_env = os.environ.copy()
    
    try:
        subprocess.Popen(vlc_cmd.split(), env=my_env)
    except:
        logger.error("Could not start process")
        return False
    return True

def check_vlc_command_line(pid):
    pid_fh = open(f"/proc/{pid}/cmdline", "r")
    cmdline = pid_fh.read().replace('\x00', ' ').rstrip()
    pid_fh.close()

    if cmdline == vlc_cmd:
        logger.debug("Found same cmd")
        return True
    else:
        logger.debug("Not same cmd")
        logger.debug(f"Proc: '{cmdline}'")
        logger.debug(f"Command: '{vlc_cmd}'")

    return False

def restart_vlc():
    """ Kill all existing pid's of active VLC and finally start new process"""
    vlc_procs = process_exists('vlc')
    if len(vlc_procs) > 0:
        for proc in vlc_procs:
            #logger.info(f"Will kill process: {proc}")
            kill_vlc_procs(proc)
    start_vlc()
    time.sleep(1)

def main():
    vlc_procs = process_exists('vlc')
    if len(vlc_procs) > 1: ## If we have more than one process we make sure to kill all
        for proc in vlc_procs:
            logger.info(f"Will kill process: {proc}")
            kill_vlc_procs(proc)
    elif len(vlc_procs) == 1:
        if not check_vlc_command_line(vlc_procs[0]):
            kill_vlc_procs(vlc_procs[0])
            start_vlc()
        else:
            print("VLC is running as it should. Nothing to do...")
    else:
        start_vlc()



if __name__ == "__main__":
    logger = Logger(name=__name__, level=verbose).get_logger()
    main()

